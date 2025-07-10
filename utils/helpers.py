import pandas as pd
import os
import pyarrow.parquet as pq
from utils.config import DATA_PATHS
from utils.logger import get_logger

logger = get_logger(__name__)

def load_zone_lookup():
    """Load taxi zone lookup data"""
    try:
        return pd.read_csv(DATA_PATHS["zone_lookup"])
    except Exception as e:
        logger.error(f"Error loading zone lookup: {e}")
        raise

def load_raw_trips():
    """Load raw trip data from parquet"""
    try:
        return pq.read_table(DATA_PATHS["raw_trips"]).to_pandas()
    except Exception as e:
        logger.error(f"Error loading raw trips: {e}")
        raise

def save_processed_data(df, file_name):
    """Save processed data to parquet"""
    try:
        path = DATA_PATHS["processed"].parent / file_name
        df.to_parquet(path)
        logger.info(f"Saved processed data to {path}")
    except Exception as e:
        logger.error(f"Error saving processed data: {e}")
        raise


def load_processed_data(filename: str) -> pd.DataFrame:
    path = os.path.join("data", "processed", filename)
    if os.path.exists(path):
        return pd.read_parquet(path)
    else:
        raise FileNotFoundError(f"Processed data not found at {path}")
