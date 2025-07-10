from confluent_kafka import Producer
import pandas as pd
import json
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.config import KAFKA_CONFIG, TOPICS, DATA_PATHS
from utils.logger import get_logger

logger = get_logger(__name__)

class KafkaProducerWrapper:
    def __init__(self, topic):
        self.producer = Producer(KAFKA_CONFIG)
        self.topic = topic

    def send(self, record):
        try:
            self.producer.produce(
                self.topic,
                key=str(record['key']),
                value=json.dumps(record['value'])
            )
            self.producer.flush()
        except Exception as e:
            logger.error(f"Failed to send record to Kafka: {e}")


    def produce_zone_data(self):
        zones = pd.read_csv(DATA_PATHS['zone_lookup'])
        for _, row in zones.iterrows():
            self.producer.produce(
                TOPICS['zones'],
                key=str(row['LocationID']),
                value=json.dumps(row.to_dict())
            )
            time.sleep(0.1)
        self.producer.flush()

    def produce_trip_data(self):
        trips = pd.read_parquet(DATA_PATHS['raw_trips'])
        for _, row in trips.sample(1000).iterrows():
            self.producer.produce(
                TOPICS['trips'],
                key=str(row['tpep_pickup_datetime']),
                value=json.dumps({
                    'VendorID': row.get('VendorID'),
                    'tpep_pickup_datetime': str(row.get('tpep_pickup_datetime')),
                    # add more fields as needed
                })
            )
            time.sleep(0.5)
        self.producer.flush()
