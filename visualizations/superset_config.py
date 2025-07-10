from sqlalchemy import create_engine
from utils.config import DB_CONFIG

def get_superset_config():
    """Configuration for Apache Superset"""
    return {
        "database_name": "taxi_demand",
        "sqlalchemy_uri": (
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        ),
        "tables": ["raw_trips", "pickup_counts", "zones"],
        "cache_timeout": 86400
    }
