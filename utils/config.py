import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Kafka Config
# Kafka Config (only Kafka client properties)
KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:29092",
    "group.id": "taxi_consumer_group"
}

# Kafka Topics
TOPICS = {
    "trips": "taxi_trips",
    "zones": "taxi_zones",
    "predictions": "taxi_predictions" ,
    "demand": "taxi_demand"
}


# Database Config
DB_CONFIG = {
    "host": "localhost",
    "database": "taxi_demand",
    "user": "postgres",
    "password": "postgres",
    "port": "5432"
}

# File Paths
DATA_PATHS = {
    "raw_trips": DATA_DIR / "raw/yellow_tripdata_2025-01.parquet",  # ← update this
    "zone_lookup": DATA_DIR / "lookup/taxi_zone_lookup.csv",
    "processed": DATA_DIR / "processed/pickup_counts.parquet"
}
