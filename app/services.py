"""
Service Layer for FinGuard Backend API.
Bridging HTTP Routes to queries.py and db.py driver lifecycle.
"""
from typing import Dict, Any, List, Optional
from neo4j import Driver
from db import get_driver, verify_connection
import queries

class DatabaseService:
    def __init__(self):
        self._driver: Optional[Driver] = None

    def initialize(self):
        """Initializes the database driver."""
        self._driver = get_driver()

    def close(self):
        """Closes the database driver cleanly."""
        if self._driver:
            self._driver.close()
            self._driver = None

    def get_driver(self) -> Driver:
        """Returns the active driver instance."""
        if not self._driver:
            self.initialize()
        return self._driver

    def check_health(self) -> Dict[str, Any]:
        """Checks database connectivity status."""
        conn_res = verify_connection(self._driver)
        return conn_res

# Singleton Service Instance
db_service = DatabaseService()

def search_entities_service(search_term: str, entity_type: Optional[str] = None) -> List[Dict[str, Any]]:
    driver = db_service.get_driver()
    return queries.search_entities(driver, search_term, entity_type)

def get_shared_device_service(device_id: str) -> Optional[Dict[str, Any]]:
    driver = db_service.get_driver()
    return queries.get_shared_device_customers(driver, device_id)

def get_shared_ip_service(ip_address: str) -> Optional[Dict[str, Any]]:
    driver = db_service.get_driver()
    return queries.get_shared_ip_customers(driver, ip_address)

def detect_circular_transfers_service(account_number: str) -> Optional[Dict[str, Any]]:
    driver = db_service.get_driver()
    return queries.detect_circular_transfers(driver, account_number)

def find_multi_hop_path_service(source_account: str, target_account: str, max_hops: int = 4) -> Optional[Dict[str, Any]]:
    driver = db_service.get_driver()
    return queries.find_multi_hop_path(driver, source_account, target_account, max_hops)

def get_high_risk_merchants_service(merchant_id: Optional[str] = None) -> List[Dict[str, Any]]:
    driver = db_service.get_driver()
    return queries.get_high_risk_merchant_exposure(driver, merchant_id)

def get_blast_radius_service(device_id: str, max_hops: int = 3) -> Optional[Dict[str, Any]]:
    driver = db_service.get_driver()
    return queries.get_device_blast_radius(driver, device_id, max_hops)

def detect_synthetic_identity_service(device_id: str, ip_address: str) -> Optional[Dict[str, Any]]:
    driver = db_service.get_driver()
    return queries.detect_synthetic_identity_cluster(driver, device_id, ip_address)

def get_neighborhood_service(entity_id: str) -> List[Dict[str, Any]]:
    driver = db_service.get_driver()
    return queries.get_entity_neighborhood(driver, entity_id)
