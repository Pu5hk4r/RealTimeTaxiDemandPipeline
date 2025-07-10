import logging
from datetime import datetime
from utils.config import BASE_DIR

# Configure logging
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"taxi_pipeline_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)

def get_logger(name):
    return logging.getLogger(name)
