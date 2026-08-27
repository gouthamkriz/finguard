"""
Connection Test Script for CognoDB Graph Database.
Purpose: Verify application communication with CognoDB safely.
"""
import sys
import neo4j
from db import load_dotenv, get_db_credentials, get_driver, verify_connection

def run_test():
    print("=" * 60)
    print("CognoDB Connection Test")
    print("=" * 60)
    
    # 1. Environment Info
    py_ver = sys.version.split()[0]
    print(f"Python Version    : {py_ver}")
    print(f"Virtual Env Path  : {sys.prefix}")
    print(f"Neo4j Driver Ver  : {neo4j.__version__}")
    print("-" * 60)
    
    # 2. Check Environment Variables
    try:
        creds = get_db_credentials()
        uri = creds["uri"]
        masked_uri = uri.split("@")[-1] if "@" in uri else uri
        print(f"COGNODB_URI       : Configured ({masked_uri})")
        print(f"COGNODB_USERNAME  : Configured ({creds['username']})")
        print(f"COGNODB_PASSWORD  : Configured (******)")
        print("-" * 60)
    except ValueError as e:
        print("\n[ERROR] Environment Setup Failure:")
        print("Category : Missing Environment Variables")
        print(f"Details  : {e}")
        print("\nTroubleshooting Action:")
        print("Please populate COGNODB_URI, COGNODB_USERNAME, and COGNODB_PASSWORD in your local .env file.")
        sys.exit(1)

    # 3. Initialize Driver & Test Connection
    print("Attempting to connect to CognoDB Cloud...")
    driver = None
    try:
        driver = get_driver()
        res = verify_connection(driver)
        
        if res["success"]:
            print("\n[SUCCESS] CognoDB Connectivity Verified!")
            print("Status       : Connected")
            print("Test Query   : RETURN 1 AS result")
            print(f"Query Result : {res['query_result']}")
        else:
            print("\n[FAIL] Connection Test Failed:")
            print(f"Category : {res.get('category', 'Unknown')}")
            print(f"Details  : {res.get('message', 'No details provided')}")
    except Exception as e:
        print(f"\n[FAIL] Connection Exception: {e}")
    finally:
        if driver:
            driver.close()
            print("Driver closed cleanly.")
    print("=" * 60)

if __name__ == "__main__":
    run_test()
