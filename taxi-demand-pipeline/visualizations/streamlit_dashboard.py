import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import DATA_PATHS
from utils.logger import get_logger



logger = get_logger(__name__)

def load_data():
    """Load processed data for visualization"""
    try:
        return pd.read_parquet(DATA_PATHS["processed"])
    except Exception as e:
        logger.error(f"Error loading data for visualization: {e}")
        st.error("Failed to load data")
        return None

def main():
    st.title("NYC Taxi Demand Dashboard")

    df = load_data()
    if df is None:
        return

    st.header("Pickup Counts by Zone")

    # Time selection
    hour = st.slider("Select hour", 0, 23, 12)
    day_of_week = st.selectbox("Select day of week", range(1, 8), 0)

    # Filter data
    filtered = df[
        (df["pickup_hour"] == hour) &
        (df["pickup_day_of_week"] == day_of_week)
        ].sort_values("pickup_count", ascending=False)

    # Top 10 zones
    st.subheader(f"Top 10 Zones (Hour: {hour}, Day: {day_of_week})")
    st.dataframe(filtered.head(10))

    # Visualization
    fig = px.bar(
        filtered.head(20),
        x="pu_location_id",
        y="pickup_count",
        color="pickup_count",
        labels={"pu_location_id": "Zone", "pickup_count": "Pickups"}
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()