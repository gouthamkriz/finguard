"""
Centralized openCypher Query Suite for FinGuard.
Source of Truth: Approved Stage 5 Design Specification.

All queries use strict parameterization with $param substitution.
Zero string concatenation or unsafe Cypher formatting.
"""
from typing import Dict, Any, List, Optional
from neo4j import Driver

# -----------------------------------------------------------------------------
# Q1: Entity Search Sub-Queries (Q1a - Q1e)
# -----------------------------------------------------------------------------

CYPHER_Q1A_CUSTOMER_SEARCH = """
MATCH (c:Customer)
WHERE c.customerId = $searchTerm OR c.name CONTAINS $searchTerm
RETURN c.customerId AS id, c.name AS name, c.riskLevel AS riskLevel, c.createdDate AS createdDate, 'Customer' AS entityType
LIMIT 10
"""

CYPHER_Q1B_ACCOUNT_SEARCH = """
MATCH (a:Account)
WHERE a.accountNumber = $searchTerm OR a.accountType = $searchTerm
RETURN a.accountNumber AS id, a.accountType AS accountType, a.status AS status, a.balance AS balance, 'Account' AS entityType
LIMIT 10
"""

CYPHER_Q1C_DEVICE_SEARCH = """
MATCH (d:Device)
WHERE d.deviceId = $searchTerm OR d.deviceType = $searchTerm
RETURN d.deviceId AS id, d.deviceType AS deviceType, d.os AS os, 'Device' AS entityType
LIMIT 10
"""

CYPHER_Q1D_IP_SEARCH = """
MATCH (i:IPAddress)
WHERE i.ipAddress = $searchTerm
RETURN i.ipAddress AS id, i.isProxy AS isProxy, 'IPAddress' AS entityType
LIMIT 10
"""

CYPHER_Q1E_MERCHANT_SEARCH = """
MATCH (m:Merchant)
WHERE m.merchantId = $searchTerm OR m.name CONTAINS $searchTerm
RETURN m.merchantId AS id, m.name AS name, m.category AS category, m.riskRating AS riskRating, 'Merchant' AS entityType
LIMIT 10
"""

def search_entities(driver: Driver, search_term: str, entity_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Executes parameterized entity searches across Customer, Account, Device, IPAddress, and Merchant nodes.
    """
    results = []
    with driver.session() as session:
        if not entity_type or entity_type.lower() == "customer":
            res = session.run(CYPHER_Q1A_CUSTOMER_SEARCH, searchTerm=search_term)
            results.extend([record.data() for record in res])
        if not entity_type or entity_type.lower() == "account":
            res = session.run(CYPHER_Q1B_ACCOUNT_SEARCH, searchTerm=search_term)
            results.extend([record.data() for record in res])
        if not entity_type or entity_type.lower() == "device":
            res = session.run(CYPHER_Q1C_DEVICE_SEARCH, searchTerm=search_term)
            results.extend([record.data() for record in res])
        if not entity_type or entity_type.lower() == "ipaddress":
            res = session.run(CYPHER_Q1D_IP_SEARCH, searchTerm=search_term)
            results.extend([record.data() for record in res])
        if not entity_type or entity_type.lower() == "merchant":
            res = session.run(CYPHER_Q1E_MERCHANT_SEARCH, searchTerm=search_term)
            results.extend([record.data() for record in res])
    return results

# -----------------------------------------------------------------------------
# Q2: Shared Device Investigation (Scenario 1)
# -----------------------------------------------------------------------------

CYPHER_Q2_SHARED_DEVICE = """
MATCH (d:Device {deviceId: $deviceId})<-[r:USED_DEVICE]-(c:Customer)
OPTIONAL MATCH (c)-[:OWNS_ACCOUNT]->(a:Account)
RETURN d.deviceId AS deviceId, d.deviceType AS deviceType, d.os AS os,
       collect({
         customerId: c.customerId,
         name: c.name,
         riskLevel: c.riskLevel,
         lastUsed: r.lastUsed,
         accountNumber: a.accountNumber
       }) AS connectedCustomers
"""

def get_shared_device_customers(driver: Driver, device_id: str) -> Optional[Dict[str, Any]]:
    with driver.session() as session:
        res = session.run(CYPHER_Q2_SHARED_DEVICE, deviceId=device_id)
        record = res.single()
        return record.data() if record else None

# -----------------------------------------------------------------------------
# Q3: Shared IP Infrastructure Investigation
# -----------------------------------------------------------------------------

CYPHER_Q3_SHARED_IP = """
MATCH (ip:IPAddress {ipAddress: $ipAddress})<-[r:LOGGED_IN_FROM]-(c:Customer)
RETURN ip.ipAddress AS ipAddress, ip.isProxy AS isProxy,
       collect({
         customerId: c.customerId,
         name: c.name,
         riskLevel: c.riskLevel,
         lastLogin: r.lastLogin,
         loginCount: r.loginCount
       }) AS connectedCustomers
"""

def get_shared_ip_customers(driver: Driver, ip_address: str) -> Optional[Dict[str, Any]]:
    with driver.session() as session:
        res = session.run(CYPHER_Q3_SHARED_IP, ipAddress=ip_address)
        record = res.single()
        return record.data() if record else None

# -----------------------------------------------------------------------------
# Q4: Circular Transfer Loop Detection (Scenario 2)
# -----------------------------------------------------------------------------

CYPHER_Q4_CIRCULAR_TRANSFER = """
MATCH (startAcc:Account {accountNumber: $accountNumber})-[t1:TRANSFERRED_FUNDS]->(mid1:Account)-[t2:TRANSFERRED_FUNDS]->(mid2:Account)-[t3:TRANSFERRED_FUNDS]->(startAcc)
WHERE mid1 <> startAcc AND mid2 <> startAcc AND mid1 <> mid2
RETURN startAcc.accountNumber AS sourceAccount,
       mid1.accountNumber AS hop1Account,
       mid2.accountNumber AS hop2Account,
       [
         {txId: t1.transactionId, amount: t1.amount, timestamp: t1.timestamp},
         {txId: t2.transactionId, amount: t2.amount, timestamp: t2.timestamp},
         {txId: t3.transactionId, amount: t3.amount, timestamp: t3.timestamp}
       ] AS transactionChain,
       3 AS cycleLength
"""

def detect_circular_transfers(driver: Driver, account_number: str) -> Optional[Dict[str, Any]]:
    with driver.session() as session:
        res = session.run(CYPHER_Q4_CIRCULAR_TRANSFER, accountNumber=account_number)
        record = res.single()
        return record.data() if record else None

# -----------------------------------------------------------------------------
# Q5: Multi-Hop Account Path Finder
# -----------------------------------------------------------------------------

CYPHER_Q5_PATH_FINDER = """
MATCH (src:Account {accountNumber: $sourceAccount}), (dest:Account {accountNumber: $targetAccount})
MATCH path = shortestPath((src)-[:TRANSFERRED_FUNDS*1..4]->(dest))
WHERE length(path) <= $maxHops
RETURN [node IN nodes(path) | node.accountNumber] AS accountChain,
       [rel IN relationships(path) | {txId: rel.transactionId, amount: rel.amount, timestamp: rel.timestamp}] AS transactionChain,
       length(path) AS totalHops
"""

def find_multi_hop_path(driver: Driver, source_account: str, target_account: str, max_hops: int = 4) -> Optional[Dict[str, Any]]:
    clamped_hops = max(1, min(max_hops, 4))
    with driver.session() as session:
        res = session.run(CYPHER_Q5_PATH_FINDER, sourceAccount=source_account, targetAccount=target_account, maxHops=clamped_hops)
        record = res.single()
        return record.data() if record else None

# -----------------------------------------------------------------------------
# Q6: High-Risk Merchant Exposure
# -----------------------------------------------------------------------------

CYPHER_Q6_HIGH_RISK_MERCHANT = """
MATCH (m:Merchant {riskRating: 'HIGH'})<-[p:PAYMENT_TO]-(a:Account)<-[:OWNS_ACCOUNT]-(c:Customer)
WHERE ($merchantId IS NULL OR m.merchantId = $merchantId)
RETURN m.merchantId AS merchantId, m.name AS merchantName, m.riskRating AS riskRating,
       a.accountNumber AS accountNumber, c.customerId AS customerId, c.name AS customerName,
       p.amount AS paymentAmount, p.timestamp AS paymentTimestamp
LIMIT 25
"""

def get_high_risk_merchant_exposure(driver: Driver, merchant_id: Optional[str] = None) -> List[Dict[str, Any]]:
    with driver.session() as session:
        res = session.run(CYPHER_Q6_HIGH_RISK_MERCHANT, merchantId=merchant_id)
        return [record.data() for record in res]

# -----------------------------------------------------------------------------
# Q7: Device Compromise Blast Radius
# -----------------------------------------------------------------------------

CYPHER_Q7_BLAST_RADIUS = """
MATCH (d:Device {deviceId: $deviceId})
MATCH path = (d)-[:USED_DEVICE|LOGGED_IN_FROM|OWNS_ACCOUNT|TRANSFERRED_FUNDS|PAYMENT_TO*1..3]-(connected)
WHERE length(path) <= $maxHops AND connected <> d
RETURN d.deviceId AS deviceId,
       collect(DISTINCT labels(connected)[0]) AS connectedEntityTypes,
       collect(DISTINCT coalesce(connected.customerId, connected.accountNumber, connected.ipAddress, connected.merchantId)) AS connectedEntityIds,
       count(DISTINCT connected) AS totalImpactedEntities,
       max(length(path)) AS maxDepthReached
"""

def get_device_blast_radius(driver: Driver, device_id: str, max_hops: int = 3) -> Optional[Dict[str, Any]]:
    clamped_hops = max(1, min(max_hops, 3))
    with driver.session() as session:
        res = session.run(CYPHER_Q7_BLAST_RADIUS, deviceId=device_id, maxHops=clamped_hops)
        record = res.single()
        return record.data() if record else None

# -----------------------------------------------------------------------------
# Q8: Synthetic Identity / Shared Infrastructure Cluster (Scenario 3)
# -----------------------------------------------------------------------------

CYPHER_Q8_SYNTHETIC_IDENTITY = """
MATCH (d:Device {deviceId: $deviceId})<-[:USED_DEVICE]-(c:Customer)-[:LOGGED_IN_FROM]->(ip:IPAddress {ipAddress: $ipAddress, isProxy: true})
MATCH (c)-[:OWNS_ACCOUNT]->(a:Account)-[p:PAYMENT_TO]->(m:Merchant {riskRating: 'HIGH'})
WITH d, ip, m, collect({customerId: c.customerId, customerName: c.name, accountNumber: a.accountNumber, paymentAmount: p.amount, paymentTimestamp: p.timestamp}) AS members, count(DISTINCT c) AS clusterSize
WHERE clusterSize > 1
RETURN d.deviceId AS sharedDevice, ip.ipAddress AS sharedIP, ip.isProxy AS isProxy,
       m.merchantId AS merchantId, m.name AS targetMerchant, m.riskRating AS riskRating,
       clusterSize AS matchedCustomerCount, members AS clusterMembers
"""

def detect_synthetic_identity_cluster(driver: Driver, device_id: str, ip_address: str) -> Optional[Dict[str, Any]]:
    with driver.session() as session:
        res = session.run(CYPHER_Q8_SYNTHETIC_IDENTITY, deviceId=device_id, ipAddress=ip_address)
        record = res.single()
        return record.data() if record else None

# -----------------------------------------------------------------------------
# Neighborhood Query (UI Graph Canvas Support)
# -----------------------------------------------------------------------------

CYPHER_NEIGHBORHOOD = """
MATCH (n)
WHERE coalesce(n.customerId, n.accountNumber, n.deviceId, n.ipAddress, n.merchantId) = $entityId
MATCH (n)-[r]-(m)
RETURN labels(n)[0] AS sourceType, coalesce(n.customerId, n.accountNumber, n.deviceId, n.ipAddress, n.merchantId) AS sourceId,
       type(r) AS relationshipType, properties(r) AS relProps,
       labels(m)[0] AS targetType, coalesce(m.customerId, m.accountNumber, m.deviceId, m.ipAddress, m.merchantId) AS targetId
LIMIT 50
"""

def get_entity_neighborhood(driver: Driver, entity_id: str) -> List[Dict[str, Any]]:
    with driver.session() as session:
        res = session.run(CYPHER_NEIGHBORHOOD, entityId=entity_id)
        return [record.data() for record in res]
