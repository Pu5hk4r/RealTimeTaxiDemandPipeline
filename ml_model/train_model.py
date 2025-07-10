import pandas as pd
import joblib
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from utils.helpers import load_processed_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transform_features(data):
    # Drop rows with missing values in key columns
    data = data.dropna(subset=["pu_location_id", "pickup_hour", "pickup_day_of_week", "pickup_count"])

    # Rename for consistency
    data = data.rename(columns={"pu_location_id": "location_id"})

    # One-hot encode location_id
    data = pd.get_dummies(data, columns=["location_id"], prefix="loc")

    # Define features and target
    X = data.drop("pickup_count", axis=1)
    y = data["pickup_count"]
    return X, y

def train_and_save_model():
    data = load_processed_data("pickup_counts.parquet")
    if data.empty:
        logger.error("Model training failed: processed data is empty.")
        return

    X, y = transform_features(data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    score = r2_score(y_test, y_pred)
    logger.info(f"Model trained with R2 score: {score:.2f}")

    # Save model and feature columns
    joblib.dump(model, "ml_model/models/taxi_demand_model.pkl")
    joblib.dump(X.columns.tolist(), "ml_model/models/model_features.pkl")

if __name__ == "__main__":
    train_and_save_model()
