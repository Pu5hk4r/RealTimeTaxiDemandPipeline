import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import logging
from confluent_kafka import Consumer, KafkaException, KafkaError
import psycopg2
from utils.config import KAFKA_CONFIG, TOPICS, DB_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)

class TaxiDataConsumer:
    def __init__(self):
        self.consumer = Consumer({
            **KAFKA_CONFIG,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False
        })
        self.db_conn = None
        self.setup_db()

    def setup_db(self):
        """Initialize PostgreSQL connection"""
        try:
            self.db_conn = psycopg2.connect(**DB_CONFIG)
            self.create_tables()
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection failed: {e}", exc_info=True)
            raise

    def create_tables(self):
        """Create required tables if they don't exist"""
        with self.db_conn.cursor() as cur:
            # Raw trips table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS raw_trips (
                    vendor_id INT,
                    tpep_pickup_datetime TIMESTAMP,
                    tpep_dropoff_datetime TIMESTAMP,
                    passenger_count INT,
                    trip_distance FLOAT,
                    pu_location_id INT,
                    do_location_id INT,
                    fare_amount FLOAT,
                    processing_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Zones table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS zones (
                    location_id INT PRIMARY KEY,
                    borough VARCHAR(50),
                    zone VARCHAR(100),
                    service_zone VARCHAR(50)
                );
            """)

            # Demand predictions table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS demand_predictions (
                prediction_id SERIAL PRIMARY KEY,
                location_id INT,
                predicted_demand FLOAT,
                borough VARCHAR(100),
                zone VARCHAR(100),
                prediction_time TIMESTAMP
           );

            """)

            self.db_conn.commit()

    def process_message(self, topic, msg):
        """Process and store incoming Kafka messages"""
        try:
            data = json.loads(msg.value())

            with self.db_conn.cursor() as cur:
                if topic == TOPICS['zones']:
                    cur.execute("""
                        INSERT INTO zones (location_id, borough, zone, service_zone)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (location_id) DO NOTHING
                    """, (
                        data['LocationID'],
                        data['Borough'],
                        data['Zone'],
                        data['service_zone']
                    ))

                elif topic == TOPICS['demand']:
                    cur.execute("""
                        INSERT INTO demand_predictions (
                            location_id, predicted_demand, borough, zone, prediction_time
                        ) VALUES (%s, %s, %s, %s, %s)
                    """, (
                        data.get('location_id'),
                        data.get('predicted_demand'),
                        data.get('borough'),
                        data.get('zone'),
                        data.get('timestamp')

                    ))
                 

                elif topic == TOPICS.get('predictions', 'taxi_demand'):
                    cur.execute("""
                        INSERT INTO demand_predictions (
                            timestamp, location_id, predicted_demand
                        ) VALUES (%s, %s, %s)
                    """, (
                        data['timestamp'],
                        data['location_id'],
                        data['predicted_demand']
                    ))

                self.db_conn.commit()
                logger.info(f"Processed message from topic '{topic}'")

        except json.JSONDecodeError as e:
            logger.error(f"Message decode error: {e}")
        except psycopg2.Error as e:
            logger.error(f"Database error: {e}")
            self.db_conn.rollback()
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)

    def consume_messages(self):
        """Main consumption loop"""
        self.consumer.subscribe(list(TOPICS.values()))
        logger.info(f"Subscribed to topics: {list(TOPICS.values())}")

        try:
            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())

                self.process_message(msg.topic(), msg)

        except KeyboardInterrupt:
            logger.info("Consumer shutting down")
        finally:
            self.close_connections()

    def close_connections(self):
        """Cleanup resources"""
        self.consumer.close()
        if self.db_conn:
            self.db_conn.close()
        logger.info("Connections closed")

if __name__ == "__main__":
    logger.info("Starting Kafka consumer")
    consumer = TaxiDataConsumer()
    consumer.consume_messages()
