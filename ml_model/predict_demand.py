import pandas as pd
import joblib
import logging
from datetime import datetime
from data_ingestion.kafka_producer import KafkaProducerWrapper
from utils.helpers import load_zone_lookup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DemandPredictor:
    def __init__(self):
        self.model = joblib.load("ml_model/models/taxi_demand_model.pkl")
        with open("ml_model/models/model_features.pkl", "rb") as f:
            self.expected_columns = joblib.load(f)

        self.zone_lookup = load_zone_lookup()
        self.kafka_producer = KafkaProducerWrapper(topic="taxi_demand")
        logger.info("Demand predictor initialized")

    def prepare_features(self, current_time: datetime) -> pd.DataFrame:
        hour = current_time.hour
        day_of_week = current_time.isoweekday()

        zones = self.zone_lookup["LocationID"].unique()
        data = pd.DataFrame({
            "pickup_hour": [hour] * len(zones),
            "pickup_day_of_week": [day_of_week] * len(zones),
            "location_id_raw": zones,
        })

        data = pd.get_dummies(data, columns=["location_id_raw"], prefix="loc")

        for col in self.expected_columns:
            if col not in data.columns:
                data[col] = 0

        data = data[self.expected_columns]
        predictions = self.model.predict(data)
        data["predicted_demand"] = predictions
        data["location_id"] = zones  # Keep original IDs for output
        return data

    def run(self):
        try:
            current_time = datetime.utcnow()
            features_df = self.prepare_features(current_time)

            for _, row in features_df.iterrows():
                location_id = int(row["location_id"])

                 #🔍 Lookup borough and zone from the zone_lookup DataFrame
                zone_info = self.zone_lookup[self.zone_lookup["LocationID"] == location_id]
                borough = zone_info["Borough"].values[0] if not zone_info.empty else "Unknown"
                zone = zone_info["Zone"].values[0] if not zone_info.empty else "Unknown"
                
                record = {
                    "key": str(int(row["location_id"])),
                    "value": {
                        "timestamp": current_time.isoformat(),
                        "location_id": int(row["location_id"]),
                        "predicted_demand": float(row["predicted_demand"]),
                        "borough":borough,
                        "zone": zone,
                    }
                }
                self.kafka_producer.send(record)

        except Exception as e:
            logger.error(f"Prediction failed: {e}", exc_info=True)

if __name__ == "__main__":
    predictor = DemandPredictor()
    predictor.run()
