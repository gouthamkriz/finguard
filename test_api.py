"""
Automated Test Suite for FinGuard FastAPI Backend API.
Source of Truth: Stage 7 Approved Specification.

Tests actual API endpoints against the running application & CognoDB database.
"""
import pytest
from fastapi.testclient import TestClient
from neo4j.exceptions import ServiceUnavailable
import app.routes as routes
from app.main import app

client = TestClient(app, raise_server_exceptions=False)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"

def test_q1_search_valid():
    response = client.get("/api/v1/search?q=Alice")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    alice = next((item for item in data if item["id"] == "CUST-A"), None)
    assert alice is not None
    assert alice["name"] == "Alice Vance"

def test_q1_search_empty():
    response = client.get("/api/v1/search?q=NONEXISTENT_TERM_9999")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_q2_shared_device_canonical():
    response = client.get("/api/v1/investigations/shared-device?deviceId=DEV-909")
    assert response.status_code == 200
    data = response.json()
    assert data["deviceId"] == "DEV-909"
    cust_ids = {c["customerId"] for c in data["connectedCustomers"]}
    assert cust_ids == {"CUST-A", "CUST-B", "CUST-C"}

def test_q3_shared_ip_canonical():
    response = client.get("/api/v1/investigations/shared-ip?ipAddress=192.0.2.45")
    assert response.status_code == 200
    data = response.json()
    assert data["ipAddress"] == "192.0.2.45"
    assert data["isProxy"] is True
    cust_ids = {c["customerId"] for c in data["connectedCustomers"]}
    assert cust_ids == {"CUST-W", "CUST-X", "CUST-Y", "CUST-Z"}

def test_q4_circular_transfer_canonical():
    response = client.get("/api/v1/investigations/circular-transfers?accountNumber=ACC-101")
    assert response.status_code == 200
    data = response.json()
    assert data["sourceAccount"] == "ACC-101"
    assert data["hop1Account"] == "ACC-202"
    assert data["hop2Account"] == "ACC-303"
    assert data["cycleLength"] == 3
    tx_ids = [tx["txId"] for tx in data["transactionChain"]]
    assert tx_ids == ["TX-1001", "TX-1002", "TX-1003"]

def test_q5_shortest_path_valid():
    response = client.get("/api/v1/investigations/shortest-path?sourceAccount=ACC-101&targetAccount=ACC-303&maxHops=4")
    assert response.status_code == 200
    data = response.json()
    assert data["accountChain"] == ["ACC-101", "ACC-202", "ACC-303"]
    assert data["totalHops"] == 2

def test_q5_shortest_path_invalid_hops():
    response = client.get("/api/v1/investigations/shortest-path?sourceAccount=ACC-101&targetAccount=ACC-303&maxHops=5")
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_q6_high_risk_merchants_canonical():
    response = client.get("/api/v1/investigations/high-risk-merchants?merchantId=MERCH-99")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 4
    for item in data:
        assert item["merchantId"] == "MERCH-99"
        assert item["riskRating"] == "HIGH"

def test_q7_blast_radius_hop1():
    response = client.get("/api/v1/investigations/blast-radius?deviceId=DEV-101&maxHops=1")
    assert response.status_code == 200
    data = response.json()
    assert data["deviceId"] == "DEV-101"
    assert data["totalImpactedEntities"] == 4
    assert data["maxDepthReached"] == 1

def test_q7_blast_radius_hop2():
    response = client.get("/api/v1/investigations/blast-radius?deviceId=DEV-101&maxHops=2")
    assert response.status_code == 200
    data = response.json()
    assert data["deviceId"] == "DEV-101"
    assert data["totalImpactedEntities"] == 9
    assert data["maxDepthReached"] == 2

def test_q7_blast_radius_hop3():
    response = client.get("/api/v1/investigations/blast-radius?deviceId=DEV-101&maxHops=3")
    assert response.status_code == 200
    data = response.json()
    assert data["deviceId"] == "DEV-101"
    assert data["totalImpactedEntities"] == 10
    assert data["maxDepthReached"] == 3

def test_q7_blast_radius_invalid_zero():
    response = client.get("/api/v1/investigations/blast-radius?deviceId=DEV-101&maxHops=0")
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_q7_blast_radius_invalid_four():
    response = client.get("/api/v1/investigations/blast-radius?deviceId=DEV-101&maxHops=4")
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_q8_synthetic_identity_canonical():
    response = client.get("/api/v1/investigations/synthetic-identity?deviceId=DEV-101&ipAddress=192.0.2.45")
    assert response.status_code == 200
    data = response.json()
    assert data["sharedDevice"] == "DEV-101"
    assert data["sharedIP"] == "192.0.2.45"
    assert data["isProxy"] is True
    assert data["merchantId"] == "MERCH-99"
    assert data["riskRating"] == "HIGH"
    assert data["matchedCustomerCount"] == 4
    cust_ids = {m["customerId"] for m in data["clusterMembers"]}
    assert cust_ids == {"CUST-W", "CUST-X", "CUST-Y", "CUST-Z"}

def test_q8_synthetic_identity_missing_params():
    response = client.get("/api/v1/investigations/synthetic-identity")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"

def test_neighborhood_endpoint():
    response = client.get("/api/v1/neighborhood?entityId=ACC-101")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_whitespace_and_oversized_identifiers_are_rejected():
    assert client.get("/api/v1/search?q=%20%20%20").status_code == 422
    assert client.get("/api/v1/investigations/shared-device?deviceId=" + "D" * 129).status_code == 422

def test_ip_and_entity_type_validation():
    assert client.get("/api/v1/investigations/shared-ip?ipAddress=not-an-ip").status_code == 422
    response = client.get("/api/v1/search?q=Alice&type=UnknownLabel")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"

def test_invalid_types_and_duplicate_parameters_are_rejected():
    assert client.get("/api/v1/investigations/blast-radius?deviceId=DEV-101&maxHops=one").status_code == 422
    response = client.get("/api/v1/investigations/blast-radius?deviceId=DEV-101&maxHops=1&maxHops=3")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"

def test_nonexistent_and_special_character_inputs_are_safe():
    response = client.get("/api/v1/investigations/shared-device?deviceId=DEV-NOT-FOUND")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"
    response = client.get("/api/v1/search?q=%E2%98%83%27%20OR%201%3D1")
    assert response.status_code == 200
    assert response.json() == []

def test_database_unavailable_error_is_safe(monkeypatch):
    def raise_unavailable(device_id):
        raise ServiceUnavailable("sensitive database endpoint")

    monkeypatch.setattr(routes, "get_shared_device_service", raise_unavailable)
    response = client.get("/api/v1/investigations/shared-device?deviceId=DEV-909")
    assert response.status_code == 503
    assert response.json() == {"error": {"code": "DATABASE_UNAVAILABLE", "message": "Database is unavailable."}}

def test_search_database_unavailable_error_is_safe(monkeypatch):
    def raise_unavailable(search_term, entity_type):
        raise ServiceUnavailable("sensitive database endpoint")

    monkeypatch.setattr(routes, "search_entities_service", raise_unavailable)
    response = client.get("/api/v1/search?q=Alice")
    assert response.status_code == 503
    assert response.json() == {"error": {"code": "DATABASE_UNAVAILABLE", "message": "Database is unavailable."}}

def test_unexpected_error_is_safe(monkeypatch):
    def raise_unexpected(device_id):
        raise RuntimeError("internal path and secret")

    monkeypatch.setattr(routes, "get_shared_device_service", raise_unexpected)
    response = client.get("/api/v1/investigations/shared-device?deviceId=DEV-909")
    assert response.status_code == 500
    assert response.json() == {"error": {"code": "QUERY_FAILED", "message": "An unexpected error occurred while processing the request."}}

if __name__ == "__main__":
    print("=" * 60)
    print("Running FinGuard API Automated Test Suite")
    print("=" * 60)
    test_health_endpoint()
    print("[PASS] test_health_endpoint")
    test_q1_search_valid()
    print("[PASS] test_q1_search_valid")
    test_q1_search_empty()
    print("[PASS] test_q1_search_empty")
    test_q2_shared_device_canonical()
    print("[PASS] test_q2_shared_device_canonical")
    test_q3_shared_ip_canonical()
    print("[PASS] test_q3_shared_ip_canonical")
    test_q4_circular_transfer_canonical()
    print("[PASS] test_q4_circular_transfer_canonical")
    test_q5_shortest_path_valid()
    print("[PASS] test_q5_shortest_path_valid")
    test_q5_shortest_path_invalid_hops()
    print("[PASS] test_q5_shortest_path_invalid_hops")
    test_q6_high_risk_merchants_canonical()
    print("[PASS] test_q6_high_risk_merchants_canonical")
    test_q7_blast_radius_hop1()
    print("[PASS] test_q7_blast_radius_hop1")
    test_q7_blast_radius_hop2()
    print("[PASS] test_q7_blast_radius_hop2")
    test_q7_blast_radius_hop3()
    print("[PASS] test_q7_blast_radius_hop3")
    test_q7_blast_radius_invalid_zero()
    print("[PASS] test_q7_blast_radius_invalid_zero")
    test_q7_blast_radius_invalid_four()
    print("[PASS] test_q7_blast_radius_invalid_four")
    test_q8_synthetic_identity_canonical()
    print("[PASS] test_q8_synthetic_identity_canonical")
    test_q8_synthetic_identity_missing_params()
    print("[PASS] test_q8_synthetic_identity_missing_params")
    test_neighborhood_endpoint()
    print("[PASS] test_neighborhood_endpoint")
    print("=" * 60)
    print("ALL API AUTOMATED TESTS PASSED PERFECTLY!")
    print("=" * 60)
