"""
Pydantic Request and Response Models for FinGuard API.
Source of Truth: Approved Stage 5 and Stage 6 Specifications.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# Generic Error & Health Models
# -----------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "ok"})
    database: str = Field(..., json_schema_extra={"example": "connected"})

class ErrorDetails(BaseModel):
    code: str = Field(..., json_schema_extra={"example": "VALIDATION_ERROR"})
    message: str = Field(..., json_schema_extra={"example": "Invalid request parameter."})

class ErrorResponse(BaseModel):
    error: ErrorDetails

# -----------------------------------------------------------------------------
# Q1: Entity Search Model
# -----------------------------------------------------------------------------

class EntitySearchResult(BaseModel):
    id: str
    entityType: str
    name: Optional[str] = None
    riskLevel: Optional[str] = None
    createdDate: Optional[str] = None
    accountType: Optional[str] = None
    status: Optional[str] = None
    balance: Optional[float] = None
    deviceType: Optional[str] = None
    os: Optional[str] = None
    isProxy: Optional[bool] = None
    category: Optional[str] = None
    riskRating: Optional[str] = None

# -----------------------------------------------------------------------------
# Q2: Shared Device Models
# -----------------------------------------------------------------------------

class SharedDeviceCustomer(BaseModel):
    customerId: str
    name: str
    riskLevel: str
    lastUsed: Optional[str] = None
    accountNumber: Optional[str] = None

class SharedDeviceResponse(BaseModel):
    deviceId: str
    deviceType: str
    os: str
    connectedCustomers: List[SharedDeviceCustomer]

# -----------------------------------------------------------------------------
# Q3: Shared IP Models
# -----------------------------------------------------------------------------

class SharedIPCustomer(BaseModel):
    customerId: str
    name: str
    riskLevel: str
    lastLogin: Optional[str] = None
    loginCount: Optional[int] = None

class SharedIPResponse(BaseModel):
    ipAddress: str
    isProxy: bool
    connectedCustomers: List[SharedIPCustomer]

# -----------------------------------------------------------------------------
# Q4 & Q5: Transaction & Path Models
# -----------------------------------------------------------------------------

class TransactionItem(BaseModel):
    txId: str
    amount: float
    timestamp: str

class CircularTransferResponse(BaseModel):
    sourceAccount: str
    hop1Account: str
    hop2Account: str
    transactionChain: List[TransactionItem]
    cycleLength: int

class ShortestPathResponse(BaseModel):
    accountChain: List[str]
    transactionChain: List[TransactionItem]
    totalHops: int

# -----------------------------------------------------------------------------
# Q6: Merchant Risk Models
# -----------------------------------------------------------------------------

class HighRiskMerchantExposure(BaseModel):
    merchantId: str
    merchantName: str
    riskRating: str
    accountNumber: str
    customerId: str
    customerName: str
    paymentAmount: float
    paymentTimestamp: str

# -----------------------------------------------------------------------------
# Q7: Blast Radius Model
# -----------------------------------------------------------------------------

class BlastRadiusResponse(BaseModel):
    deviceId: str
    connectedEntityTypes: List[str]
    connectedEntityIds: List[str]
    totalImpactedEntities: int
    maxDepthReached: int

# -----------------------------------------------------------------------------
# Q8: Synthetic Identity Cluster Models
# -----------------------------------------------------------------------------

class ClusterMember(BaseModel):
    customerId: str
    customerName: str
    accountNumber: str
    paymentAmount: float
    paymentTimestamp: str

class SyntheticIdentityClusterResponse(BaseModel):
    sharedDevice: str
    sharedIP: str
    isProxy: bool
    merchantId: str
    targetMerchant: str
    riskRating: str
    matchedCustomerCount: int
    clusterMembers: List[ClusterMember]

# -----------------------------------------------------------------------------
# Neighborhood Edge Model
# -----------------------------------------------------------------------------

class NeighborhoodEdge(BaseModel):
    sourceType: str
    sourceId: str
    relationshipType: str
    relProps: Dict[str, Any]
    targetType: str
    targetId: str
