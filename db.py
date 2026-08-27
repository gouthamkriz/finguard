"""
Database Connection Module for CognoDB Graph Database.
Uses official Neo4j Python driver and Bolt protocol.
"""
import os
import sys
from typing import Dict, Any, Optional
from neo4j import GraphDatabase, Driver
from neo4j.exceptions import (
    AuthError,
    ServiceUnavailable,
    ConfigurationError,
    Neo4jError,
)

def load_dotenv(filepath: str = ".env") -> None:
    """
    Lightweight zero-dependency .env loader.
    Reads key=value pairs into os.environ without overwriting existing environment variables.
    """
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    if key and key not in os.environ:
                        os.environ[key] = val

def get_db_credentials() -> Dict[str, str]:
    """
    Retrieves and validates CognoDB connection parameters from environment variables.
    Raises ValueError with safe error messages if required variables are missing.
    """
    load_dotenv()
    
    uri = os.getenv("COGNODB_URI")
    username = os.getenv("COGNODB_USERNAME", "cognodb")
    password = os.getenv("COGNODB_PASSWORD")
    
    missing = []
    if not uri or not uri.strip():
        missing.append("COGNODB_URI")
    if not username or not username.strip():
        missing.append("COGNODB_USERNAME")
    if not password or not password.strip():
        missing.append("COGNODB_PASSWORD")
        
    if missing:
        raise ValueError(
            f"Missing required database environment variable(s): {', '.join(missing)}. "
            f"Please populate these variables in your local .env file."
        )
        
    return {
        "uri": uri.strip(),
        "username": username.strip(),
        "password": password.strip(),
    }

def get_driver() -> Driver:
    """
    Creates and returns a Neo4j Driver instance configured for CognoDB.
    Does not expose sensitive credentials in error traces.
    """
    creds = get_db_credentials()
    try:
        driver = GraphDatabase.driver(
            creds["uri"],
            auth=(creds["username"], creds["password"]),
        )
        return driver
    except ConfigurationError as e:
        raise ValueError(f"Invalid CognoDB driver configuration / URI format: {e}") from None
    except Exception:
        raise RuntimeError("Failed to initialize Neo4j database driver.") from None

def verify_connection(driver: Optional[Driver] = None) -> Dict[str, Any]:
    """
    Verifies connectivity to the CognoDB instance and executes a minimal test query.
    Categorizes errors safely without leaking sensitive information.
    """
    close_after = False
    if driver is None:
        driver = get_driver()
        close_after = True
        
    try:
        # Verify driver network connectivity
        driver.verify_connectivity()
        
        # Execute minimal harmless query: RETURN 1 AS result
        with driver.session() as session:
            result = session.run("RETURN 1 AS result")
            record = result.single()
            query_val = record["result"] if record else None
            
        return {
            "success": True,
            "query_result": query_val,
            "message": "Successfully connected to CognoDB and executed test query."
        }
    except AuthError:
        return {
            "success": False,
            "category": "Invalid Credentials",
            "message": "Authentication failed. Please verify COGNODB_USERNAME and COGNODB_PASSWORD."
        }
    except ServiceUnavailable as e:
        return {
            "success": False,
            "category": "Database Unavailable / Network Error",
            "message": f"Could not connect to CognoDB at specified URI. Details: {e}"
        }
    except ConfigurationError as e:
        return {
            "success": False,
            "category": "Invalid URI / Configuration Error",
            "message": f"Invalid driver configuration or URI. Details: {e}"
        }
    except Neo4jError as e:
        return {
            "success": False,
            "category": "Database Query Error",
            "message": f"CognoDB query error: {e.code} - {e.message}"
        }
    except Exception:
        return {
            "success": False,
            "category": "Unexpected Connection Failure",
            "message": "An unexpected error occurred during database verification."
        }
    finally:
        if close_after and driver:
            driver.close()
