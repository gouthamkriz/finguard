"""
Deterministic Seed Data Specification for FinGuard.
Source of Truth: Stage 5 Approved Design Report.

Nodes:
- 25 Customers (CUST-A..C, CUST-W..Z, CUST-01..18)
- 28 Accounts (ACC-101..303, ACC-401..404, ACC-01..21)
- 12 Devices (DEV-909, DEV-101, DEV-01..10)
- 12 IPAddresses (192.0.2.45, 198.51.100.1..11)
- 10 Merchants (MERCH-99, MERCH-01..09)
Total Nodes = 87

Relationships:
- 28 OWNS_ACCOUNT
- 30 USED_DEVICE
- 30 LOGGED_IN_FROM
- 35 TRANSFERRED_FUNDS
- 15 PAYMENT_TO
Total Relationships = 138
"""

CUSTOMERS = [
    # Scenario 1 & 2
    {"customerId": "CUST-A", "name": "Alice Vance", "riskLevel": "MEDIUM", "createdDate": "2026-01-10T08:00:00Z"},
    {"customerId": "CUST-B", "name": "Bob Smith", "riskLevel": "MEDIUM", "createdDate": "2026-01-12T09:30:00Z"},
    {"customerId": "CUST-C", "name": "Charlie Davis", "riskLevel": "MEDIUM", "createdDate": "2026-01-15T11:15:00Z"},
    # Scenario 3
    {"customerId": "CUST-W", "name": "William West", "riskLevel": "HIGH", "createdDate": "2026-02-01T14:00:00Z"},
    {"customerId": "CUST-X", "name": "Xavier Drake", "riskLevel": "HIGH", "createdDate": "2026-02-01T14:05:00Z"},
    {"customerId": "CUST-Y", "name": "Yvonne Young", "riskLevel": "HIGH", "createdDate": "2026-02-01T14:10:00Z"},
    {"customerId": "CUST-Z", "name": "Zachary Zane", "riskLevel": "HIGH", "createdDate": "2026-02-01T14:15:00Z"},
    # Benign Customers (18)
    {"customerId": "CUST-01", "name": "Daniel Evans", "riskLevel": "LOW", "createdDate": "2026-01-05T10:00:00Z"},
    {"customerId": "CUST-02", "name": "Emily Frost", "riskLevel": "LOW", "createdDate": "2026-01-06T10:30:00Z"},
    {"customerId": "CUST-03", "name": "Frank Green", "riskLevel": "LOW", "createdDate": "2026-01-07T11:00:00Z"},
    {"customerId": "CUST-04", "name": "Grace Hopper", "riskLevel": "LOW", "createdDate": "2026-01-08T11:30:00Z"},
    {"customerId": "CUST-05", "name": "Henry Ivy", "riskLevel": "LOW", "createdDate": "2026-01-09T12:00:00Z"},
    {"customerId": "CUST-06", "name": "Isla Jones", "riskLevel": "LOW", "createdDate": "2026-01-10T12:30:00Z"},
    {"customerId": "CUST-07", "name": "Jack King", "riskLevel": "LOW", "createdDate": "2026-01-11T13:00:00Z"},
    {"customerId": "CUST-08", "name": "Karen Lane", "riskLevel": "LOW", "createdDate": "2026-01-12T13:30:00Z"},
    {"customerId": "CUST-09", "name": "Leo Miller", "riskLevel": "LOW", "createdDate": "2026-01-13T14:00:00Z"},
    {"customerId": "CUST-10", "name": "Mia Nelson", "riskLevel": "MEDIUM", "createdDate": "2026-01-14T14:30:00Z"},
    {"customerId": "CUST-11", "name": "Noah Owens", "riskLevel": "LOW", "createdDate": "2026-01-15T15:00:00Z"},
    {"customerId": "CUST-12", "name": "Olivia Park", "riskLevel": "LOW", "createdDate": "2026-01-16T15:30:00Z"},
    {"customerId": "CUST-13", "name": "Peter Quinn", "riskLevel": "LOW", "createdDate": "2026-01-17T16:00:00Z"},
    {"customerId": "CUST-14", "name": "Rachel Ross", "riskLevel": "MEDIUM", "createdDate": "2026-01-18T16:30:00Z"},
    {"customerId": "CUST-15", "name": "Samuel Scott", "riskLevel": "LOW", "createdDate": "2026-01-19T17:00:00Z"},
    {"customerId": "CUST-16", "name": "Tina Taylor", "riskLevel": "LOW", "createdDate": "2026-01-20T17:30:00Z"},
    {"customerId": "CUST-17", "name": "Victor Underwood", "riskLevel": "MEDIUM", "createdDate": "2026-01-21T18:00:00Z"},
    {"customerId": "CUST-18", "name": "Wendy Vance", "riskLevel": "LOW", "createdDate": "2026-01-22T18:30:00Z"},
]

ACCOUNTS = [
    # Scenario 1 & 2
    {"accountNumber": "ACC-101", "accountType": "CHECKING", "status": "ACTIVE", "balance": 15400.00},
    {"accountNumber": "ACC-202", "accountType": "SAVINGS", "status": "ACTIVE", "balance": 8200.00},
    {"accountNumber": "ACC-303", "accountType": "CHECKING", "status": "ACTIVE", "balance": 12000.00},
    # Scenario 3
    {"accountNumber": "ACC-401", "accountType": "CHECKING", "status": "ACTIVE", "balance": 4500.00},
    {"accountNumber": "ACC-402", "accountType": "CHECKING", "status": "ACTIVE", "balance": 5100.00},
    {"accountNumber": "ACC-403", "accountType": "CHECKING", "status": "ACTIVE", "balance": 3900.00},
    {"accountNumber": "ACC-404", "accountType": "CHECKING", "status": "ACTIVE", "balance": 6200.00},
    # Benign Accounts (21)
    {"accountNumber": "ACC-01", "accountType": "CHECKING", "status": "ACTIVE", "balance": 5000.00},
    {"accountNumber": "ACC-02", "accountType": "SAVINGS", "status": "ACTIVE", "balance": 12500.00},
    {"accountNumber": "ACC-03", "accountType": "CHECKING", "status": "ACTIVE", "balance": 3200.00},
    {"accountNumber": "ACC-04", "accountType": "SAVINGS", "status": "ACTIVE", "balance": 9800.00},
    {"accountNumber": "ACC-05", "accountType": "CHECKING", "status": "ACTIVE", "balance": 7400.00},
    {"accountNumber": "ACC-06", "accountType": "SAVINGS", "status": "ACTIVE", "balance": 15000.00},
    {"accountNumber": "ACC-07", "accountType": "CHECKING", "status": "ACTIVE", "balance": 4100.00},
    {"accountNumber": "ACC-08", "accountType": "SAVINGS", "status": "ACTIVE", "balance": 6300.00},
    {"accountNumber": "ACC-09", "accountType": "CHECKING", "status": "ACTIVE", "balance": 8900.00},
    {"accountNumber": "ACC-10", "accountType": "CHECKING", "status": "ACTIVE", "balance": 2100.00},
    {"accountNumber": "ACC-11", "accountType": "SAVINGS", "status": "ACTIVE", "balance": 11200.00},
    {"accountNumber": "ACC-12", "accountType": "CHECKING", "status": "ACTIVE", "balance": 5400.00},
    {"accountNumber": "ACC-13", "accountType": "SAVINGS", "status": "ACTIVE", "balance": 7800.00},
    {"accountNumber": "ACC-14", "accountType": "CHECKING", "status": "SUSPENDED", "balance": 1500.00},
    {"accountNumber": "ACC-15", "accountType": "SAVINGS", "status": "ACTIVE", "balance": 14300.00},
    {"accountNumber": "ACC-16", "accountType": "CHECKING", "status": "ACTIVE", "balance": 3700.00},
    {"accountNumber": "ACC-17", "accountType": "SAVINGS", "status": "ACTIVE", "balance": 8400.00},
    {"accountNumber": "ACC-18", "accountType": "CHECKING", "status": "ACTIVE", "balance": 9100.00},
    {"accountNumber": "ACC-19", "accountType": "CHECKING", "status": "ACTIVE", "balance": 6700.00},
    {"accountNumber": "ACC-20", "accountType": "SAVINGS", "status": "FROZEN", "balance": 500.00},
    {"accountNumber": "ACC-21", "accountType": "CHECKING", "status": "ACTIVE", "balance": 10500.00},
]

DEVICES = [
    # Scenario 1
    {"deviceId": "DEV-909", "deviceType": "MOBILE_IOS", "os": "iOS 17.4"},
    # Scenario 3
    {"deviceId": "DEV-101", "deviceType": "DESKTOP_WINDOWS", "os": "Windows 11"},
    # Benign Devices (10)
    {"deviceId": "DEV-01", "deviceType": "MOBILE_IOS", "os": "iOS 17.2"},
    {"deviceId": "DEV-02", "deviceType": "MOBILE_ANDROID", "os": "Android 14"},
    {"deviceId": "DEV-03", "deviceType": "DESKTOP_WINDOWS", "os": "Windows 11"},
    {"deviceId": "DEV-04", "deviceType": "MOBILE_IOS", "os": "iOS 17.3"},
    {"deviceId": "DEV-05", "deviceType": "MOBILE_ANDROID", "os": "Android 13"},
    {"deviceId": "DEV-06", "deviceType": "DESKTOP_WINDOWS", "os": "Windows 10"},
    {"deviceId": "DEV-07", "deviceType": "MOBILE_IOS", "os": "iOS 16.7"},
    {"deviceId": "DEV-08", "deviceType": "MOBILE_ANDROID", "os": "Android 14"},
    {"deviceId": "DEV-09", "deviceType": "DESKTOP_WINDOWS", "os": "Windows 11"},
    {"deviceId": "DEV-10", "deviceType": "MOBILE_IOS", "os": "iOS 17.4"},
]

IP_ADDRESSES = [
    # Scenario 3
    {"ipAddress": "192.0.2.45", "isProxy": True},
    # Benign IPs (11)
    {"ipAddress": "198.51.100.1", "isProxy": False},
    {"ipAddress": "198.51.100.2", "isProxy": False},
    {"ipAddress": "198.51.100.3", "isProxy": False},
    {"ipAddress": "198.51.100.4", "isProxy": False},
    {"ipAddress": "198.51.100.5", "isProxy": False},
    {"ipAddress": "198.51.100.6", "isProxy": False},
    {"ipAddress": "198.51.100.7", "isProxy": False},
    {"ipAddress": "198.51.100.8", "isProxy": False},
    {"ipAddress": "198.51.100.9", "isProxy": False},
    {"ipAddress": "198.51.100.10", "isProxy": False},
    {"ipAddress": "198.51.100.11", "isProxy": False},
]

MERCHANTS = [
    # Scenario 3
    {"merchantId": "MERCH-99", "name": "Apex Crypto Exchange", "category": "CRYPTO_EXCHANGE", "riskRating": "HIGH"},
    # Benign Merchants (9)
    {"merchantId": "MERCH-01", "name": "Global Retail Direct", "category": "E_COMMERCE", "riskRating": "LOW"},
    {"merchantId": "MERCH-02", "name": "City Power & Light", "category": "E_COMMERCE", "riskRating": "LOW"},
    {"merchantId": "MERCH-03", "name": "Swift Wire Transfer Services", "category": "WIRE_TRANSFER", "riskRating": "MEDIUM"},
    {"merchantId": "MERCH-04", "name": "Metro Transit Pass", "category": "E_COMMERCE", "riskRating": "LOW"},
    {"merchantId": "MERCH-05", "name": "Harbor Freight Goods", "category": "E_COMMERCE", "riskRating": "LOW"},
    {"merchantId": "MERCH-06", "name": "Digital Stream TV", "category": "E_COMMERCE", "riskRating": "LOW"},
    {"merchantId": "MERCH-07", "name": "FastCash Remittance", "category": "WIRE_TRANSFER", "riskRating": "MEDIUM"},
    {"merchantId": "MERCH-08", "name": "Summit Outdoor Gear", "category": "E_COMMERCE", "riskRating": "LOW"},
    {"merchantId": "MERCH-09", "name": "Prime Supermarket", "category": "E_COMMERCE", "riskRating": "LOW"},
]

OWNS_ACCOUNT_RELATIONS = [
    # Scenario 1 & 2 (3)
    {"customerId": "CUST-A", "accountNumber": "ACC-101", "isPrimary": True, "ownedSince": "2026-01-10T08:00:00Z"},
    {"customerId": "CUST-B", "accountNumber": "ACC-202", "isPrimary": True, "ownedSince": "2026-01-12T09:30:00Z"},
    {"customerId": "CUST-C", "accountNumber": "ACC-303", "isPrimary": True, "ownedSince": "2026-01-15T11:15:00Z"},
    # Scenario 3 (4)
    {"customerId": "CUST-W", "accountNumber": "ACC-401", "isPrimary": True, "ownedSince": "2026-02-01T14:00:00Z"},
    {"customerId": "CUST-X", "accountNumber": "ACC-402", "isPrimary": True, "ownedSince": "2026-02-01T14:05:00Z"},
    {"customerId": "CUST-Y", "accountNumber": "ACC-403", "isPrimary": True, "ownedSince": "2026-02-01T14:10:00Z"},
    {"customerId": "CUST-Z", "accountNumber": "ACC-404", "isPrimary": True, "ownedSince": "2026-02-01T14:15:00Z"},
    # Benign Accounts (21)
    {"customerId": "CUST-01", "accountNumber": "ACC-01", "isPrimary": True, "ownedSince": "2026-01-05T10:00:00Z"},
    {"customerId": "CUST-01", "accountNumber": "ACC-02", "isPrimary": False, "ownedSince": "2026-01-05T10:00:00Z"},
    {"customerId": "CUST-02", "accountNumber": "ACC-03", "isPrimary": True, "ownedSince": "2026-01-06T10:30:00Z"},
    {"customerId": "CUST-02", "accountNumber": "ACC-04", "isPrimary": False, "ownedSince": "2026-01-06T10:30:00Z"},
    {"customerId": "CUST-03", "accountNumber": "ACC-05", "isPrimary": True, "ownedSince": "2026-01-07T11:00:00Z"},
    {"customerId": "CUST-03", "accountNumber": "ACC-06", "isPrimary": False, "ownedSince": "2026-01-07T11:00:00Z"},
    {"customerId": "CUST-04", "accountNumber": "ACC-07", "isPrimary": True, "ownedSince": "2026-01-08T11:30:00Z"},
    {"customerId": "CUST-05", "accountNumber": "ACC-08", "isPrimary": True, "ownedSince": "2026-01-09T12:00:00Z"},
    {"customerId": "CUST-06", "accountNumber": "ACC-09", "isPrimary": True, "ownedSince": "2026-01-10T12:30:00Z"},
    {"customerId": "CUST-07", "accountNumber": "ACC-10", "isPrimary": True, "ownedSince": "2026-01-11T13:00:00Z"},
    {"customerId": "CUST-08", "accountNumber": "ACC-11", "isPrimary": True, "ownedSince": "2026-01-12T13:30:00Z"},
    {"customerId": "CUST-09", "accountNumber": "ACC-12", "isPrimary": True, "ownedSince": "2026-01-13T14:00:00Z"},
    {"customerId": "CUST-10", "accountNumber": "ACC-13", "isPrimary": True, "ownedSince": "2026-01-14T14:30:00Z"},
    {"customerId": "CUST-11", "accountNumber": "ACC-14", "isPrimary": True, "ownedSince": "2026-01-15T15:00:00Z"},
    {"customerId": "CUST-12", "accountNumber": "ACC-15", "isPrimary": True, "ownedSince": "2026-01-16T15:30:00Z"},
    {"customerId": "CUST-13", "accountNumber": "ACC-16", "isPrimary": True, "ownedSince": "2026-01-17T16:00:00Z"},
    {"customerId": "CUST-14", "accountNumber": "ACC-17", "isPrimary": True, "ownedSince": "2026-01-18T16:30:00Z"},
    {"customerId": "CUST-15", "accountNumber": "ACC-18", "isPrimary": True, "ownedSince": "2026-01-19T17:00:00Z"},
    {"customerId": "CUST-16", "accountNumber": "ACC-19", "isPrimary": True, "ownedSince": "2026-01-20T17:30:00Z"},
    {"customerId": "CUST-17", "accountNumber": "ACC-20", "isPrimary": True, "ownedSince": "2026-01-21T18:00:00Z"},
    {"customerId": "CUST-18", "accountNumber": "ACC-21", "isPrimary": True, "ownedSince": "2026-01-22T18:30:00Z"},
]

USED_DEVICE_RELATIONS = [
    # Scenario 1 (3)
    {"customerId": "CUST-A", "deviceId": "DEV-909", "lastUsed": "2026-08-25T12:00:00Z"},
    {"customerId": "CUST-B", "deviceId": "DEV-909", "lastUsed": "2026-08-25T12:05:00Z"},
    {"customerId": "CUST-C", "deviceId": "DEV-909", "lastUsed": "2026-08-25T12:10:00Z"},
    # Scenario 3 (4)
    {"customerId": "CUST-W", "deviceId": "DEV-101", "lastUsed": "2026-08-26T16:00:00Z"},
    {"customerId": "CUST-X", "deviceId": "DEV-101", "lastUsed": "2026-08-26T16:05:00Z"},
    {"customerId": "CUST-Y", "deviceId": "DEV-101", "lastUsed": "2026-08-26T16:10:00Z"},
    {"customerId": "CUST-Z", "deviceId": "DEV-101", "lastUsed": "2026-08-26T16:15:00Z"},
    # Benign Devices (23)
    {"customerId": "CUST-01", "deviceId": "DEV-01", "lastUsed": "2026-08-20T09:00:00Z"},
    {"customerId": "CUST-01", "deviceId": "DEV-02", "lastUsed": "2026-08-21T10:00:00Z"},
    {"customerId": "CUST-02", "deviceId": "DEV-02", "lastUsed": "2026-08-20T11:00:00Z"},
    {"customerId": "CUST-02", "deviceId": "DEV-03", "lastUsed": "2026-08-21T12:00:00Z"},
    {"customerId": "CUST-03", "deviceId": "DEV-03", "lastUsed": "2026-08-20T13:00:00Z"},
    {"customerId": "CUST-03", "deviceId": "DEV-04", "lastUsed": "2026-08-21T14:00:00Z"},
    {"customerId": "CUST-04", "deviceId": "DEV-04", "lastUsed": "2026-08-20T15:00:00Z"},
    {"customerId": "CUST-04", "deviceId": "DEV-05", "lastUsed": "2026-08-21T16:00:00Z"},
    {"customerId": "CUST-05", "deviceId": "DEV-05", "lastUsed": "2026-08-20T17:00:00Z"},
    {"customerId": "CUST-05", "deviceId": "DEV-06", "lastUsed": "2026-08-21T18:00:00Z"},
    {"customerId": "CUST-06", "deviceId": "DEV-06", "lastUsed": "2026-08-22T09:00:00Z"},
    {"customerId": "CUST-07", "deviceId": "DEV-06", "lastUsed": "2026-08-22T10:00:00Z"},
    {"customerId": "CUST-08", "deviceId": "DEV-07", "lastUsed": "2026-08-22T11:00:00Z"},
    {"customerId": "CUST-09", "deviceId": "DEV-07", "lastUsed": "2026-08-22T12:00:00Z"},
    {"customerId": "CUST-10", "deviceId": "DEV-07", "lastUsed": "2026-08-22T13:00:00Z"},
    {"customerId": "CUST-11", "deviceId": "DEV-08", "lastUsed": "2026-08-23T09:00:00Z"},
    {"customerId": "CUST-12", "deviceId": "DEV-08", "lastUsed": "2026-08-23T10:00:00Z"},
    {"customerId": "CUST-13", "deviceId": "DEV-08", "lastUsed": "2026-08-23T11:00:00Z"},
    {"customerId": "CUST-14", "deviceId": "DEV-09", "lastUsed": "2026-08-24T09:00:00Z"},
    {"customerId": "CUST-15", "deviceId": "DEV-09", "lastUsed": "2026-08-24T10:00:00Z"},
    {"customerId": "CUST-16", "deviceId": "DEV-09", "lastUsed": "2026-08-24T11:00:00Z"},
    {"customerId": "CUST-17", "deviceId": "DEV-10", "lastUsed": "2026-08-24T12:00:00Z"},
    {"customerId": "CUST-18", "deviceId": "DEV-10", "lastUsed": "2026-08-24T13:00:00Z"},
]

LOGGED_IN_FROM_RELATIONS = [
    # Scenario 3 Proxy IP (4)
    {"customerId": "CUST-W", "ipAddress": "192.0.2.45", "lastLogin": "2026-08-26T16:00:00Z", "loginCount": 14},
    {"customerId": "CUST-X", "ipAddress": "192.0.2.45", "lastLogin": "2026-08-26T16:05:00Z", "loginCount": 12},
    {"customerId": "CUST-Y", "ipAddress": "192.0.2.45", "lastLogin": "2026-08-26T16:10:00Z", "loginCount": 15},
    {"customerId": "CUST-Z", "ipAddress": "192.0.2.45", "lastLogin": "2026-08-26T16:15:00Z", "loginCount": 10},
    # Scenario 1 Home IPs (3)
    {"customerId": "CUST-A", "ipAddress": "198.51.100.1", "lastLogin": "2026-08-25T12:00:00Z", "loginCount": 25},
    {"customerId": "CUST-B", "ipAddress": "198.51.100.2", "lastLogin": "2026-08-25T12:05:00Z", "loginCount": 18},
    {"customerId": "CUST-C", "ipAddress": "198.51.100.3", "lastLogin": "2026-08-25T12:10:00Z", "loginCount": 22},
    # Benign IPs (23)
    {"customerId": "CUST-01", "ipAddress": "198.51.100.1", "lastLogin": "2026-08-20T09:00:00Z", "loginCount": 5},
    {"customerId": "CUST-01", "ipAddress": "198.51.100.2", "lastLogin": "2026-08-21T10:00:00Z", "loginCount": 8},
    {"customerId": "CUST-02", "ipAddress": "198.51.100.2", "lastLogin": "2026-08-20T11:00:00Z", "loginCount": 4},
    {"customerId": "CUST-02", "ipAddress": "198.51.100.3", "lastLogin": "2026-08-21T12:00:00Z", "loginCount": 6},
    {"customerId": "CUST-03", "ipAddress": "198.51.100.3", "lastLogin": "2026-08-20T13:00:00Z", "loginCount": 7},
    {"customerId": "CUST-03", "ipAddress": "198.51.100.4", "lastLogin": "2026-08-21T14:00:00Z", "loginCount": 9},
    {"customerId": "CUST-04", "ipAddress": "198.51.100.4", "lastLogin": "2026-08-20T15:00:00Z", "loginCount": 11},
    {"customerId": "CUST-04", "ipAddress": "198.51.100.5", "lastLogin": "2026-08-21T16:00:00Z", "loginCount": 3},
    {"customerId": "CUST-05", "ipAddress": "198.51.100.5", "lastLogin": "2026-08-20T17:00:00Z", "loginCount": 12},
    {"customerId": "CUST-05", "ipAddress": "198.51.100.6", "lastLogin": "2026-08-21T18:00:00Z", "loginCount": 15},
    {"customerId": "CUST-06", "ipAddress": "198.51.100.6", "lastLogin": "2026-08-22T09:00:00Z", "loginCount": 8},
    {"customerId": "CUST-07", "ipAddress": "198.51.100.6", "lastLogin": "2026-08-22T10:00:00Z", "loginCount": 10},
    {"customerId": "CUST-08", "ipAddress": "198.51.100.7", "lastLogin": "2026-08-22T11:00:00Z", "loginCount": 6},
    {"customerId": "CUST-09", "ipAddress": "198.51.100.7", "lastLogin": "2026-08-22T12:00:00Z", "loginCount": 7},
    {"customerId": "CUST-10", "ipAddress": "198.51.100.7", "lastLogin": "2026-08-22T13:00:00Z", "loginCount": 9},
    {"customerId": "CUST-11", "ipAddress": "198.51.100.8", "lastLogin": "2026-08-23T09:00:00Z", "loginCount": 4},
    {"customerId": "CUST-12", "ipAddress": "198.51.100.8", "lastLogin": "2026-08-23T10:00:00Z", "loginCount": 5},
    {"customerId": "CUST-13", "ipAddress": "198.51.100.8", "lastLogin": "2026-08-23T11:00:00Z", "loginCount": 8},
    {"customerId": "CUST-14", "ipAddress": "198.51.100.9", "lastLogin": "2026-08-24T09:00:00Z", "loginCount": 14},
    {"customerId": "CUST-15", "ipAddress": "198.51.100.9", "lastLogin": "2026-08-24T10:00:00Z", "loginCount": 11},
    {"customerId": "CUST-16", "ipAddress": "198.51.100.9", "lastLogin": "2026-08-24T11:00:00Z", "loginCount": 13},
    {"customerId": "CUST-17", "ipAddress": "198.51.100.10", "lastLogin": "2026-08-24T12:00:00Z", "loginCount": 16},
    {"customerId": "CUST-18", "ipAddress": "198.51.100.11", "lastLogin": "2026-08-24T13:00:00Z", "loginCount": 19},
]

TRANSFERRED_FUNDS_RELATIONS = [
    # Scenario 2 Circular Loop (3)
    {"sourceAccount": "ACC-101", "targetAccount": "ACC-202", "transactionId": "TX-1001", "amount": 5000.00, "timestamp": "2026-08-25T10:00:00Z"},
    {"sourceAccount": "ACC-202", "targetAccount": "ACC-303", "transactionId": "TX-1002", "amount": 4800.00, "timestamp": "2026-08-25T14:30:00Z"},
    {"sourceAccount": "ACC-303", "targetAccount": "ACC-101", "transactionId": "TX-1003", "amount": 4500.00, "timestamp": "2026-08-26T09:15:00Z"},
    # Scenario 3 Setup Internal Transfers (4)
    {"sourceAccount": "ACC-401", "targetAccount": "ACC-402", "transactionId": "TX-4001A", "amount": 1200.00, "timestamp": "2026-08-26T12:00:00Z"},
    {"sourceAccount": "ACC-402", "targetAccount": "ACC-403", "transactionId": "TX-4002A", "amount": 1100.00, "timestamp": "2026-08-26T13:00:00Z"},
    {"sourceAccount": "ACC-403", "targetAccount": "ACC-404", "transactionId": "TX-4003A", "amount": 1000.00, "timestamp": "2026-08-26T14:00:00Z"},
    {"sourceAccount": "ACC-404", "targetAccount": "ACC-401", "transactionId": "TX-4004A", "amount": 900.00, "timestamp": "2026-08-26T15:00:00Z"},
    # Benign Transfers (28)
    {"sourceAccount": "ACC-01", "targetAccount": "ACC-02", "transactionId": "TX-0001", "amount": 250.00, "timestamp": "2026-08-10T10:00:00Z"},
    {"sourceAccount": "ACC-02", "targetAccount": "ACC-03", "transactionId": "TX-0002", "amount": 400.00, "timestamp": "2026-08-11T11:00:00Z"},
    {"sourceAccount": "ACC-03", "targetAccount": "ACC-04", "transactionId": "TX-0003", "amount": 150.00, "timestamp": "2026-08-12T12:00:00Z"},
    {"sourceAccount": "ACC-04", "targetAccount": "ACC-05", "transactionId": "TX-0004", "amount": 600.00, "timestamp": "2026-08-13T13:00:00Z"},
    {"sourceAccount": "ACC-05", "targetAccount": "ACC-06", "transactionId": "TX-0005", "amount": 800.00, "timestamp": "2026-08-14T14:00:00Z"},
    {"sourceAccount": "ACC-06", "targetAccount": "ACC-07", "transactionId": "TX-0006", "amount": 350.00, "timestamp": "2026-08-15T15:00:00Z"},
    {"sourceAccount": "ACC-07", "targetAccount": "ACC-08", "transactionId": "TX-0007", "amount": 900.00, "timestamp": "2026-08-16T16:00:00Z"},
    {"sourceAccount": "ACC-08", "targetAccount": "ACC-09", "transactionId": "TX-0008", "amount": 120.00, "timestamp": "2026-08-17T17:00:00Z"},
    {"sourceAccount": "ACC-09", "targetAccount": "ACC-10", "transactionId": "TX-0009", "amount": 550.00, "timestamp": "2026-08-18T18:00:00Z"},
    {"sourceAccount": "ACC-10", "targetAccount": "ACC-11", "transactionId": "TX-0010", "amount": 750.00, "timestamp": "2026-08-19T09:00:00Z"},
    {"sourceAccount": "ACC-11", "targetAccount": "ACC-12", "transactionId": "TX-0011", "amount": 300.00, "timestamp": "2026-08-20T10:00:00Z"},
    {"sourceAccount": "ACC-12", "targetAccount": "ACC-13", "transactionId": "TX-0012", "amount": 450.00, "timestamp": "2026-08-21T11:00:00Z"},
    {"sourceAccount": "ACC-13", "targetAccount": "ACC-14", "transactionId": "TX-0013", "amount": 200.00, "timestamp": "2026-08-22T12:00:00Z"},
    {"sourceAccount": "ACC-14", "targetAccount": "ACC-15", "transactionId": "TX-0014", "amount": 650.00, "timestamp": "2026-08-23T13:00:00Z"},
    {"sourceAccount": "ACC-15", "targetAccount": "ACC-16", "transactionId": "TX-0015", "amount": 1100.00, "timestamp": "2026-08-24T14:00:00Z"},
    {"sourceAccount": "ACC-16", "targetAccount": "ACC-17", "transactionId": "TX-0016", "amount": 180.00, "timestamp": "2026-08-24T15:00:00Z"},
    {"sourceAccount": "ACC-17", "targetAccount": "ACC-18", "transactionId": "TX-0017", "amount": 820.00, "timestamp": "2026-08-24T16:00:00Z"},
    {"sourceAccount": "ACC-18", "targetAccount": "ACC-19", "transactionId": "TX-0018", "amount": 940.00, "timestamp": "2026-08-24T17:00:00Z"},
    {"sourceAccount": "ACC-19", "targetAccount": "ACC-20", "transactionId": "TX-0019", "amount": 310.00, "timestamp": "2026-08-24T18:00:00Z"},
    {"sourceAccount": "ACC-20", "targetAccount": "ACC-21", "transactionId": "TX-0020", "amount": 500.00, "timestamp": "2026-08-25T09:00:00Z"},
    {"sourceAccount": "ACC-01", "targetAccount": "ACC-03", "transactionId": "TX-0021", "amount": 1250.00, "timestamp": "2026-08-25T11:00:00Z"},
    {"sourceAccount": "ACC-03", "targetAccount": "ACC-05", "transactionId": "TX-0022", "amount": 720.00, "timestamp": "2026-08-25T13:00:00Z"},
    {"sourceAccount": "ACC-05", "targetAccount": "ACC-07", "transactionId": "TX-0023", "amount": 430.00, "timestamp": "2026-08-25T15:00:00Z"},
    {"sourceAccount": "ACC-07", "targetAccount": "ACC-09", "transactionId": "TX-0024", "amount": 880.00, "timestamp": "2026-08-25T17:00:00Z"},
    {"sourceAccount": "ACC-09", "targetAccount": "ACC-11", "transactionId": "TX-0025", "amount": 640.00, "timestamp": "2026-08-26T10:00:00Z"},
    {"sourceAccount": "ACC-11", "targetAccount": "ACC-13", "transactionId": "TX-0026", "amount": 390.00, "timestamp": "2026-08-26T11:00:00Z"},
    {"sourceAccount": "ACC-13", "targetAccount": "ACC-15", "transactionId": "TX-0027", "amount": 1050.00, "timestamp": "2026-08-26T12:00:00Z"},
    {"sourceAccount": "ACC-15", "targetAccount": "ACC-17", "transactionId": "TX-0028", "amount": 770.00, "timestamp": "2026-08-26T14:00:00Z"},
]

PAYMENT_TO_RELATIONS = [
    # Scenario 3 Cash-out Payments (4)
    {"accountNumber": "ACC-401", "merchantId": "MERCH-99", "transactionId": "TX-4001", "amount": 2500.00, "timestamp": "2026-08-26T18:00:00Z"},
    {"accountNumber": "ACC-402", "merchantId": "MERCH-99", "transactionId": "TX-4002", "amount": 3100.00, "timestamp": "2026-08-26T18:05:00Z"},
    {"accountNumber": "ACC-403", "merchantId": "MERCH-99", "transactionId": "TX-4003", "amount": 1900.00, "timestamp": "2026-08-26T18:10:00Z"},
    {"accountNumber": "ACC-404", "merchantId": "MERCH-99", "transactionId": "TX-4004", "amount": 4200.00, "timestamp": "2026-08-26T18:15:00Z"},
    # Benign Payments (11)
    {"accountNumber": "ACC-01", "merchantId": "MERCH-01", "transactionId": "TX-P001", "amount": 85.50, "timestamp": "2026-08-20T10:00:00Z"},
    {"accountNumber": "ACC-02", "merchantId": "MERCH-02", "transactionId": "TX-P002", "amount": 140.00, "timestamp": "2026-08-20T11:00:00Z"},
    {"accountNumber": "ACC-03", "merchantId": "MERCH-03", "transactionId": "TX-P003", "amount": 350.00, "timestamp": "2026-08-21T12:00:00Z"},
    {"accountNumber": "ACC-04", "merchantId": "MERCH-04", "transactionId": "TX-P004", "amount": 45.00, "timestamp": "2026-08-21T13:00:00Z"},
    {"accountNumber": "ACC-05", "merchantId": "MERCH-05", "transactionId": "TX-P005", "amount": 220.00, "timestamp": "2026-08-22T14:00:00Z"},
    {"accountNumber": "ACC-06", "merchantId": "MERCH-06", "transactionId": "TX-P006", "amount": 29.99, "timestamp": "2026-08-22T15:00:00Z"},
    {"accountNumber": "ACC-07", "merchantId": "MERCH-07", "transactionId": "TX-P007", "amount": 500.00, "timestamp": "2026-08-23T16:00:00Z"},
    {"accountNumber": "ACC-08", "merchantId": "MERCH-08", "transactionId": "TX-P008", "amount": 175.00, "timestamp": "2026-08-23T17:00:00Z"},
    {"accountNumber": "ACC-09", "merchantId": "MERCH-09", "transactionId": "TX-P009", "amount": 92.40, "timestamp": "2026-08-24T18:00:00Z"},
    {"accountNumber": "ACC-10", "merchantId": "MERCH-01", "transactionId": "TX-P010", "amount": 115.00, "timestamp": "2026-08-24T19:00:00Z"},
    {"accountNumber": "ACC-11", "merchantId": "MERCH-02", "transactionId": "TX-P011", "amount": 160.00, "timestamp": "2026-08-25T08:00:00Z"},
]
