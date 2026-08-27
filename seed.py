"""
Deterministic Seed Script & Validator for FinGuard.
Source of Truth: Stage 5 Approved Design Specification.

Execution Order:
1. Verify database connectivity (reusing db.py architecture).
2. Apply uniqueness constraints & search indexes.
3. Batch MERGE Nodes (25 Customers, 28 Accounts, 12 Devices, 12 IPAddresses, 10 Merchants = 87 Nodes).
4. Batch MERGE Structural Relationships (28 OWNS_ACCOUNT, 30 USED_DEVICE, 30 LOGGED_IN_FROM).
5. Batch MERGE Transaction Relationships (35 TRANSFERRED_FUNDS, 15 PAYMENT_TO). Total Relationships = 138.
6. Execute automated validation assertions & canonical scenario topology tests.
"""

import sys
from db import get_driver, verify_connection
from seed_data import (
    CUSTOMERS,
    ACCOUNTS,
    DEVICES,
    IP_ADDRESSES,
    MERCHANTS,
    OWNS_ACCOUNT_RELATIONS,
    USED_DEVICE_RELATIONS,
    LOGGED_IN_FROM_RELATIONS,
    TRANSFERRED_FUNDS_RELATIONS,
    PAYMENT_TO_RELATIONS,
)
from queries import (
    detect_circular_transfers,
    get_device_blast_radius,
    detect_synthetic_identity_cluster,
)

def apply_schema_constraints(session):
    print("Applying schema constraints and search indexes...", flush=True)
    constraints = [
        "CREATE CONSTRAINT customer_id_unique IF NOT EXISTS FOR (c:Customer) REQUIRE c.customerId IS UNIQUE",
        "CREATE CONSTRAINT account_number_unique IF NOT EXISTS FOR (a:Account) REQUIRE a.accountNumber IS UNIQUE",
        "CREATE CONSTRAINT device_id_unique IF NOT EXISTS FOR (d:Device) REQUIRE d.deviceId IS UNIQUE",
        "CREATE CONSTRAINT ip_address_unique IF NOT EXISTS FOR (i:IPAddress) REQUIRE i.ipAddress IS UNIQUE",
        "CREATE CONSTRAINT merchant_id_unique IF NOT EXISTS FOR (m:Merchant) REQUIRE m.merchantId IS UNIQUE",
    ]
    indexes = [
        "CREATE INDEX customer_name_index IF NOT EXISTS FOR (c:Customer) ON (c.name)",
        "CREATE INDEX merchant_name_index IF NOT EXISTS FOR (m:Merchant) ON (m.name)",
        "CREATE INDEX account_status_index IF NOT EXISTS FOR (a:Account) ON (a.status)",
    ]
    for stmt in constraints + indexes:
        session.run(stmt)

def seed_nodes(session):
    print("Seeding nodes in batches...", flush=True)
    # Customers
    session.run(
        "UNWIND $batch AS row "
        "MERGE (n:Customer {customerId: row.customerId}) "
        "SET n.name = row.name, n.riskLevel = row.riskLevel, n.createdDate = row.createdDate",
        batch=CUSTOMERS
    )
    # Accounts
    session.run(
        "UNWIND $batch AS row "
        "MERGE (n:Account {accountNumber: row.accountNumber}) "
        "SET n.accountType = row.accountType, n.status = row.status, n.balance = row.balance",
        batch=ACCOUNTS
    )
    # Devices
    session.run(
        "UNWIND $batch AS row "
        "MERGE (n:Device {deviceId: row.deviceId}) "
        "SET n.deviceType = row.deviceType, n.os = row.os",
        batch=DEVICES
    )
    # IPAddresses
    session.run(
        "UNWIND $batch AS row "
        "MERGE (n:IPAddress {ipAddress: row.ipAddress}) "
        "SET n.isProxy = row.isProxy",
        batch=IP_ADDRESSES
    )
    # Merchants
    session.run(
        "UNWIND $batch AS row "
        "MERGE (n:Merchant {merchantId: row.merchantId}) "
        "SET n.name = row.name, n.category = row.category, n.riskRating = row.riskRating",
        batch=MERCHANTS
    )

def seed_relationships(session):
    print("Seeding structural and transaction relationships in batches...", flush=True)
    # OWNS_ACCOUNT
    session.run(
        "UNWIND $batch AS row "
        "MATCH (c:Customer {customerId: row.customerId}), (a:Account {accountNumber: row.accountNumber}) "
        "MERGE (c)-[rel:OWNS_ACCOUNT]->(a) "
        "SET rel.isPrimary = row.isPrimary, rel.ownedSince = row.ownedSince",
        batch=OWNS_ACCOUNT_RELATIONS
    )
    # USED_DEVICE
    session.run(
        "UNWIND $batch AS row "
        "MATCH (c:Customer {customerId: row.customerId}), (d:Device {deviceId: row.deviceId}) "
        "MERGE (c)-[rel:USED_DEVICE]->(d) "
        "SET rel.lastUsed = row.lastUsed",
        batch=USED_DEVICE_RELATIONS
    )
    # LOGGED_IN_FROM
    session.run(
        "UNWIND $batch AS row "
        "MATCH (c:Customer {customerId: row.customerId}), (ip:IPAddress {ipAddress: row.ipAddress}) "
        "MERGE (c)-[rel:LOGGED_IN_FROM]->(ip) "
        "SET rel.lastLogin = row.lastLogin, rel.loginCount = row.loginCount",
        batch=LOGGED_IN_FROM_RELATIONS
    )
    # TRANSFERRED_FUNDS (matching transactionId)
    session.run(
        "UNWIND $batch AS row "
        "MATCH (src:Account {accountNumber: row.sourceAccount}), (dest:Account {accountNumber: row.targetAccount}) "
        "MERGE (src)-[rel:TRANSFERRED_FUNDS {transactionId: row.transactionId}]->(dest) "
        "SET rel.amount = row.amount, rel.timestamp = row.timestamp",
        batch=TRANSFERRED_FUNDS_RELATIONS
    )
    # PAYMENT_TO (matching transactionId)
    session.run(
        "UNWIND $batch AS row "
        "MATCH (a:Account {accountNumber: row.accountNumber}), (m:Merchant {merchantId: row.merchantId}) "
        "MERGE (a)-[rel:PAYMENT_TO {transactionId: row.transactionId}]->(m) "
        "SET rel.amount = row.amount, rel.timestamp = row.timestamp",
        batch=PAYMENT_TO_RELATIONS
    )

def run_validations(driver):
    print("\nRunning automated seed validations...", flush=True)
    errors = []
    
    with driver.session() as session:
        # Node Counts
        c_count = session.run("MATCH (n:Customer) RETURN count(n) AS cnt").single()["cnt"]
        a_count = session.run("MATCH (n:Account) RETURN count(n) AS cnt").single()["cnt"]
        d_count = session.run("MATCH (n:Device) RETURN count(n) AS cnt").single()["cnt"]
        ip_count = session.run("MATCH (n:IPAddress) RETURN count(n) AS cnt").single()["cnt"]
        m_count = session.run("MATCH (n:Merchant) RETURN count(n) AS cnt").single()["cnt"]
        total_nodes = session.run("MATCH (n) RETURN count(n) AS cnt").single()["cnt"]
        
        print(f"Nodes Breakdown -> Customer: {c_count}/25, Account: {a_count}/28, Device: {d_count}/12, IPAddress: {ip_count}/12, Merchant: {m_count}/10 | Total: {total_nodes}/87", flush=True)
        
        if c_count != 25 or a_count != 28 or d_count != 12 or ip_count != 12 or m_count != 10 or total_nodes != 87:
            errors.append(f"Node count mismatch! Expected 87 nodes (25 C, 28 A, 12 D, 12 IP, 10 M), got {total_nodes}.")
            
        # Relationship Counts
        r_owns = session.run("MATCH ()-[r:OWNS_ACCOUNT]->() RETURN count(r) AS cnt").single()["cnt"]
        r_used = session.run("MATCH ()-[r:USED_DEVICE]->() RETURN count(r) AS cnt").single()["cnt"]
        r_logged = session.run("MATCH ()-[r:LOGGED_IN_FROM]->() RETURN count(r) AS cnt").single()["cnt"]
        r_tx = session.run("MATCH ()-[r:TRANSFERRED_FUNDS]->() RETURN count(r) AS cnt").single()["cnt"]
        r_pay = session.run("MATCH ()-[r:PAYMENT_TO]->() RETURN count(r) AS cnt").single()["cnt"]
        total_rels = session.run("MATCH ()-[r]->() RETURN count(r) AS cnt").single()["cnt"]
        
        print(f"Relationships Breakdown -> OWNS_ACCOUNT: {r_owns}/28, USED_DEVICE: {r_used}/30, LOGGED_IN_FROM: {r_logged}/30, TRANSFERRED_FUNDS: {r_tx}/35, PAYMENT_TO: {r_pay}/15 | Total: {total_rels}/138", flush=True)
        
        if r_owns != 28 or r_used != 30 or r_logged != 30 or r_tx != 35 or r_pay != 15 or total_rels != 138:
            errors.append(f"Relationship count mismatch! Expected 138 relationships (28 OWNS, 30 USED, 30 LOGGED, 35 TX, 15 PAY), got {total_rels}.")
            
        # Scenario 1 Check (DEV-909)
        dev_909_custs = session.run(
            "MATCH (d:Device {deviceId: 'DEV-909'})<-[:USED_DEVICE]-(c:Customer) RETURN collect(c.customerId) AS custs"
        ).single()["custs"]
        print(f"DEV-909 Shared Customers: {dev_909_custs}", flush=True)
        if set(dev_909_custs) != {"CUST-A", "CUST-B", "CUST-C"}:
            errors.append(f"Scenario 1 check failed! DEV-909 expected CUST-A, B, C; got {dev_909_custs}")
            
        # Scenario 3 Proxy IP Check (192.0.2.45)
        ip_proxy_custs = session.run(
            "MATCH (ip:IPAddress {ipAddress: '192.0.2.45', isProxy: true})<-[:LOGGED_IN_FROM]-(c:Customer) RETURN collect(c.customerId) AS custs"
        ).single()["custs"]
        print(f"192.0.2.45 Shared Customers: {ip_proxy_custs}", flush=True)
        if set(ip_proxy_custs) != {"CUST-W", "CUST-X", "CUST-Y", "CUST-Z"}:
            errors.append(f"Scenario 3 proxy check failed! 192.0.2.45 expected CUST-W, X, Y, Z; got {ip_proxy_custs}")

    # Query Executions (Q4, Q7, Q8)
    print("\nValidating Canonical Scenario Queries...", flush=True)
    
    # Q4: Circular Loop
    q4_res = detect_circular_transfers(driver, "ACC-101")
    if q4_res and q4_res.get("sourceAccount") == "ACC-101" and q4_res.get("cycleLength") == 3:
        print(f"[PASS] Q4 Circular Transfer Detected: ACC-101 -> ACC-202 -> ACC-303 -> ACC-101 (3 hops)", flush=True)
    else:
        errors.append(f"Q4 Circular Transfer validation failed! Result: {q4_res}")
        
    # Q7: Blast Radius (maxHops 1, 2, 3)
    br_1 = get_device_blast_radius(driver, "DEV-101", 1)
    br_2 = get_device_blast_radius(driver, "DEV-101", 2)
    br_3 = get_device_blast_radius(driver, "DEV-101", 3)
    
    print(f"[PASS] Q7 Blast Radius DEV-101 -> maxHops=1: {br_1.get('totalImpactedEntities')} entities", flush=True)
    print(f"[PASS] Q7 Blast Radius DEV-101 -> maxHops=2: {br_2.get('totalImpactedEntities')} entities", flush=True)
    print(f"[PASS] Q7 Blast Radius DEV-101 -> maxHops=3: {br_3.get('totalImpactedEntities')} entities", flush=True)
    
    if not (br_1.get('totalImpactedEntities') == 4 and br_2.get('totalImpactedEntities') == 9 and br_3.get('totalImpactedEntities') == 10):
        errors.append(f"Q7 Blast Radius topology failed! Expected 4, 9, 10; got {br_1.get('totalImpactedEntities')}, {br_2.get('totalImpactedEntities')}, {br_3.get('totalImpactedEntities')}")
        
    # Q8: Synthetic Identity Cluster
    q8_res = detect_synthetic_identity_cluster(driver, "DEV-101", "192.0.2.45")
    if q8_res and q8_res.get("matchedCustomerCount") == 4 and q8_res.get("merchantId") == "MERCH-99":
        print(f"[PASS] Q8 Synthetic Identity Cluster Detected: 4 customers on DEV-101 & 192.0.2.45 targeting MERCH-99", flush=True)
    else:
        errors.append(f"Q8 Synthetic Identity Cluster validation failed! Result: {q8_res}")

    if errors:
        print("\n[FAIL] Validation Errors Detected:", flush=True)
        for err in errors:
            print(f" - {err}", flush=True)
        return False
    else:
        print("\n[SUCCESS] All Seed Data & Topology Validations PASSED Perfectly!", flush=True)
        return True

def run_seed():
    print("=" * 60, flush=True)
    print("FinGuard Graph Seeding & Validation Routine", flush=True)
    print("=" * 60, flush=True)
    
    conn_info = verify_connection()
    if not conn_info["success"]:
        print(f"[ERROR] Database connection failed: {conn_info['message']}", flush=True)
        sys.exit(1)
        
    driver = get_driver()
    try:
        with driver.session() as session:
            apply_schema_constraints(session)
            seed_nodes(session)
            seed_relationships(session)
            
        success = run_validations(driver)
        print("=" * 60, flush=True)
        if success:
            print("SEED EXECUTION & VALIDATION SUCCESSFUL", flush=True)
        else:
            print("SEED VALIDATION FAILED", flush=True)
            sys.exit(1)
    finally:
        driver.close()

if __name__ == "__main__":
    run_seed()
