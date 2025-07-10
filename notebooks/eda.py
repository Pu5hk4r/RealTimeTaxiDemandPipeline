
# notebooks/eda.py
import pandas as pd
import matplotlib.pyplot as plt
from utils.config import DATA_PATHS
from utils.logger import get_logger

logger = get_logger(__name__)

def load_data():
    """Load raw trip and zone data"""
    try:
        trips = pd.read_parquet(DATA_PATHS['raw_trips'])
        zones = pd.read_csv(DATA_PATHS['zone_lookup'])
        logger.info("Data loaded successfully")
        return trips, zones
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

def analyze_trips(trips):
    """Perform basic trip analysis"""
    print("\n=== Basic Trip Statistics ===")
    print(f"Total trips: {len(trips):,}")
    print("\nSummary Statistics:")
    print(trips[['trip_distance', 'passenger_count', 'fare_amount']].describe())

def plot_distance_distribution(trips):
    """Plot histogram of trip distances"""
    plt.figure(figsize=(10, 6))
    trips['trip_distance'].hist(bins=50, range=(0, 50))
    plt.title('Trip Distance Distribution')
    plt.xlabel('Distance (miles)')
    plt.ylabel('Count')
    plt.savefig(DATA_PATHS['processed'].parent / 'trip_distance_distribution.png')
    logger.info("Saved distance distribution plot")

def analyze_pickup_locations(trips, zones):
    """Analyze popular pickup locations"""
    pickup_counts = trips['PULocationID'].value_counts().reset_index()
    pickup_counts.columns = ['LocationID', 'Count']
    pickup_counts = pickup_counts.merge(zones, on='LocationID')

    print("\n=== Top 10 Pickup Locations ===")
    print(pickup_counts.head(10))

    return pickup_counts

def main():
    """Main EDA workflow"""
    logger.info("Starting EDA analysis")
    trips, zones = load_data()

    analyze_trips(trips)
    plot_distance_distribution(trips)
    pickup_counts = analyze_pickup_locations(trips, zones)

    logger.info("EDA completed successfully")

if __name__ == "__main__":
    main()