"""
FastAPI Routes for FinGuard Graph Intelligence API.
"""
from ipaddress import IPv4Address
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.models import (
    HealthResponse,
    ErrorResponse,
    EntitySearchResult,
    SharedDeviceResponse,
    SharedIPResponse,
    CircularTransferResponse,
    ShortestPathResponse,
    HighRiskMerchantExposure,
    BlastRadiusResponse,
    SyntheticIdentityClusterResponse,
    NeighborhoodEdge,
)
from app.services import (
    db_service,
    search_entities_service,
    get_shared_device_service,
    get_shared_ip_service,
    detect_circular_transfers_service,
    find_multi_hop_path_service,
    get_high_risk_merchants_service,
    get_blast_radius_service,
    detect_synthetic_identity_service,
    get_neighborhood_service,
)

router = APIRouter()

IDENTIFIER_MAX_LENGTH = 128
SEARCH_MAX_LENGTH = 256
NON_WHITESPACE_PATTERN = r".*\S.*"
ALLOWED_ENTITY_TYPES = {"customer", "account", "device", "ipaddress", "merchant"}

VALIDATION_ERROR_RESPONSE = {"model": ErrorResponse, "description": "Invalid request parameter."}
NOT_FOUND_ERROR_RESPONSE = {"model": ErrorResponse, "description": "Requested entity or relationship pattern was not found."}
DATABASE_ERROR_RESPONSE = {"model": ErrorResponse, "description": "CognoDB is unavailable."}
QUERY_ERROR_RESPONSE = {"model": ErrorResponse, "description": "Unexpected query processing failure."}

# -----------------------------------------------------------------------------
# Health Check Endpoint
# -----------------------------------------------------------------------------

@router.get("/health", response_model=HealthResponse, tags=["Health"], summary="Check API and database health", responses={503: DATABASE_ERROR_RESPONSE})
def health_check():
    """
    Returns API runtime health and CognoDB connection status.
    """
    health = db_service.check_health()
    if not health.get("success"):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "DATABASE_UNAVAILABLE", "message": "Database is unavailable."}
        )
    return HealthResponse(status="ok", database="connected")

# -----------------------------------------------------------------------------
# Q1: Entity Search API
# -----------------------------------------------------------------------------

@router.get("/api/v1/search", response_model=List[EntitySearchResult], tags=["Search"], summary="Search graph entities", responses={422: VALIDATION_ERROR_RESPONSE, 500: QUERY_ERROR_RESPONSE, 503: DATABASE_ERROR_RESPONSE})
def search_entities(
    q: str = Query(..., description="Search term for ID or name (1–256 non-whitespace characters)", min_length=1, max_length=SEARCH_MAX_LENGTH, pattern=NON_WHITESPACE_PATTERN),
    type: Optional[str] = Query(None, description="Optional entity filter: Customer, Account, Device, IPAddress, or Merchant", max_length=IDENTIFIER_MAX_LENGTH, pattern=NON_WHITESPACE_PATTERN)
):
    """
    Searches entities across Customer, Account, Device, IPAddress, and Merchant labels.
    """
    if type and type.lower() not in ALLOWED_ENTITY_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={"code": "VALIDATION_ERROR", "message": "type must be Customer, Account, Device, IPAddress, or Merchant."},
        )
    return search_entities_service(q, type)

# -----------------------------------------------------------------------------
# Q2: Shared Device Investigation API (Scenario 1)
# -----------------------------------------------------------------------------

@router.get("/api/v1/investigations/shared-device", response_model=SharedDeviceResponse, tags=["Investigations"], summary="Find customers sharing a device", responses={404: NOT_FOUND_ERROR_RESPONSE, 422: VALIDATION_ERROR_RESPONSE, 503: DATABASE_ERROR_RESPONSE})
def get_shared_device(
    deviceId: str = Query(..., description="Hardware device fingerprint ID (1–128 non-whitespace characters)", min_length=1, max_length=IDENTIFIER_MAX_LENGTH, pattern=NON_WHITESPACE_PATTERN)
):
    """
    Retrieves customer profiles connected to a shared hardware device.
    """
    res = get_shared_device_service(deviceId)
    if not res or not res.get("deviceId"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"Device '{deviceId}' not found or has no linked usage records."}
        )
    return res

# -----------------------------------------------------------------------------
# Q3: Shared IP Infrastructure Investigation API
# -----------------------------------------------------------------------------

@router.get("/api/v1/investigations/shared-ip", response_model=SharedIPResponse, tags=["Investigations"], summary="Find customers sharing an IPv4 address", responses={404: NOT_FOUND_ERROR_RESPONSE, 422: VALIDATION_ERROR_RESPONSE, 503: DATABASE_ERROR_RESPONSE})
def get_shared_ip(
    ipAddress: IPv4Address = Query(..., description="Network IPv4 access point address")
):
    """
    Retrieves customer profiles logged in from a shared IP address or proxy.
    """
    ip_address = str(ipAddress)
    res = get_shared_ip_service(ip_address)
    if not res or not res.get("ipAddress"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"IP Address '{ip_address}' not found or has no linked login logs."}
        )
    return res

# -----------------------------------------------------------------------------
# Q4: Circular Transfer Loop Detection API (Scenario 2)
# -----------------------------------------------------------------------------

@router.get("/api/v1/investigations/circular-transfers", response_model=CircularTransferResponse, tags=["Investigations"], summary="Detect a three-account circular transfer", responses={404: NOT_FOUND_ERROR_RESPONSE, 422: VALIDATION_ERROR_RESPONSE, 503: DATABASE_ERROR_RESPONSE})
def detect_circular_transfers(
    accountNumber: str = Query(..., description="Target bank account number (1–128 non-whitespace characters)", min_length=1, max_length=IDENTIFIER_MAX_LENGTH, pattern=NON_WHITESPACE_PATTERN)
):
    """
    Detects 3-account circular transfer loops originating from the target account.
    """
    res = detect_circular_transfers_service(accountNumber)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"No circular transfer loop detected for account '{accountNumber}'."}
        )
    return res

# -----------------------------------------------------------------------------
# Q5: Multi-Hop Shortest Path Finder API
# -----------------------------------------------------------------------------

@router.get("/api/v1/investigations/shortest-path", response_model=ShortestPathResponse, tags=["Investigations"], summary="Find a bounded shortest transfer path", responses={400: VALIDATION_ERROR_RESPONSE, 404: NOT_FOUND_ERROR_RESPONSE, 422: VALIDATION_ERROR_RESPONSE, 503: DATABASE_ERROR_RESPONSE})
def find_multi_hop_path(
    sourceAccount: str = Query(..., description="Source account number (1–128 non-whitespace characters)", min_length=1, max_length=IDENTIFIER_MAX_LENGTH, pattern=NON_WHITESPACE_PATTERN),
    targetAccount: str = Query(..., description="Destination account number (1–128 non-whitespace characters)", min_length=1, max_length=IDENTIFIER_MAX_LENGTH, pattern=NON_WHITESPACE_PATTERN),
    maxHops: int = Query(4, description="Maximum traversal depth (1 to 4 hops)")
):
    """
    Finds the shortest transaction transfer path between two accounts.
    """
    if maxHops < 1 or maxHops > 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "VALIDATION_ERROR", "message": "maxHops must be an integer between 1 and 4."}
        )
    res = find_multi_hop_path_service(sourceAccount, targetAccount, maxHops)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"No transfer path found from '{sourceAccount}' to '{targetAccount}' within {maxHops} hops."}
        )
    return res

# -----------------------------------------------------------------------------
# Q6: High-Risk Merchant Exposure API
# -----------------------------------------------------------------------------

@router.get("/api/v1/investigations/high-risk-merchants", response_model=List[HighRiskMerchantExposure], tags=["Investigations"], summary="List exposure to high-risk merchants", responses={422: VALIDATION_ERROR_RESPONSE, 503: DATABASE_ERROR_RESPONSE})
def get_high_risk_merchants(
    merchantId: Optional[str] = Query(None, description="Optional merchant ID filter (1–128 non-whitespace characters)", max_length=IDENTIFIER_MAX_LENGTH, pattern=NON_WHITESPACE_PATTERN)
):
    """
    Retrieves customer account payments directed to HIGH risk rating merchants.
    """
    results = get_high_risk_merchants_service(merchantId)
    return results

# -----------------------------------------------------------------------------
# Q7: Device Compromise Blast Radius API
# -----------------------------------------------------------------------------

@router.get("/api/v1/investigations/blast-radius", response_model=BlastRadiusResponse, tags=["Investigations"], summary="Calculate a bounded device blast radius", responses={400: VALIDATION_ERROR_RESPONSE, 404: NOT_FOUND_ERROR_RESPONSE, 422: VALIDATION_ERROR_RESPONSE, 503: DATABASE_ERROR_RESPONSE})
def get_device_blast_radius(
    deviceId: str = Query(..., description="Target hardware device ID (1–128 non-whitespace characters)", min_length=1, max_length=IDENTIFIER_MAX_LENGTH, pattern=NON_WHITESPACE_PATTERN),
    maxHops: int = Query(3, description="Maximum graph traversal depth (1 to 3 hops)")
):
    """
    Computes the network blast radius of entities connected to a device within N hops.
    """
    if maxHops < 1 or maxHops > 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "VALIDATION_ERROR", "message": "maxHops must be an integer between 1 and 3."}
        )
    res = get_blast_radius_service(deviceId, maxHops)
    if not res or not res.get("deviceId"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"Device '{deviceId}' not found or has no blast radius network."}
        )
    return res

# -----------------------------------------------------------------------------
# Q8: Synthetic Identity Cluster API (Scenario 3)
# -----------------------------------------------------------------------------

@router.get("/api/v1/investigations/synthetic-identity", response_model=SyntheticIdentityClusterResponse, tags=["Investigations"], summary="Detect a synthetic identity cluster", responses={404: NOT_FOUND_ERROR_RESPONSE, 422: VALIDATION_ERROR_RESPONSE, 503: DATABASE_ERROR_RESPONSE})
def detect_synthetic_identity_cluster(
    deviceId: str = Query(..., description="Shared device ID (1–128 non-whitespace characters)", min_length=1, max_length=IDENTIFIER_MAX_LENGTH, pattern=NON_WHITESPACE_PATTERN),
    ipAddress: IPv4Address = Query(..., description="Shared proxy IPv4 address")
):
    """
    Detects synthetic identity clusters sharing both a device and proxy IP while paying high-risk merchants.
    """
    ip_address = str(ipAddress)
    res = detect_synthetic_identity_service(deviceId, ip_address)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": f"No synthetic identity cluster detected for device '{deviceId}' and IP '{ip_address}'."}
        )
    return res

# -----------------------------------------------------------------------------
# Entity Neighborhood API (Graph Canvas Support)
# -----------------------------------------------------------------------------

@router.get("/api/v1/neighborhood", response_model=List[NeighborhoodEdge], tags=["Graph Visualization"], summary="Get an entity's one-hop neighborhood", responses={422: VALIDATION_ERROR_RESPONSE, 503: DATABASE_ERROR_RESPONSE})
def get_entity_neighborhood(
    entityId: str = Query(..., description="Node primary key identifier (1–128 non-whitespace characters)", min_length=1, max_length=IDENTIFIER_MAX_LENGTH, pattern=NON_WHITESPACE_PATTERN)
):
    """
    Returns immediate 1-hop graph edges for visual rendering on the graph canvas.
    """
    results = get_neighborhood_service(entityId)
    return results
