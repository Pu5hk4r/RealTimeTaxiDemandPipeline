-- ========================
-- Raw trip data table
-- ========================
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

-- Indexes for raw_trips
CREATE INDEX IF NOT EXISTS idx_pu_location ON raw_trips(pu_location_id);
CREATE INDEX IF NOT EXISTS idx_pickup_time ON raw_trips(tpep_pickup_datetime);

-- ========================
-- Taxi zone lookup table
-- ========================
CREATE TABLE IF NOT EXISTS zones (
    location_id INT PRIMARY KEY,
    borough VARCHAR(50),
    zone VARCHAR(100),
    service_zone VARCHAR(50)
);

-- Index for borough
CREATE INDEX IF NOT EXISTS idx_borough ON zones(borough);

-- ========================
-- Processed pickup counts
-- ========================
CREATE TABLE IF NOT EXISTS pickup_counts (
    pu_location_id INT,
    pickup_hour INT,
    pickup_day_of_week INT,
    pickup_count INT,
    processing_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (pu_location_id, pickup_hour, pickup_day_of_week),
    FOREIGN KEY (pu_location_id) REFERENCES zones(location_id)
);

-- ========================
-- Demand predictions table
-- ========================
CREATE TABLE IF NOT EXISTS demand_predictions (
    prediction_id SERIAL PRIMARY KEY,
    location_id INT,
    predicted_demand INT,
    prediction_time TIMESTAMP,
    borough VARCHAR(50),
    zone VARCHAR(100),
    UNIQUE (location_id, prediction_time),
    FOREIGN KEY (location_id) REFERENCES zones(location_id)
);

-- Indexes for predictions
CREATE INDEX IF NOT EXISTS idx_prediction_time ON demand_predictions(prediction_time);
CREATE INDEX IF NOT EXISTS idx_location_pred ON demand_predictions(location_id, prediction_time);

-- ========================
-- Materialized View
-- ========================
CREATE MATERIALIZED VIEW IF NOT EXISTS demand_forecasts AS
SELECT
    dp.location_id,
    z.zone,
    z.borough,
    dp.predicted_demand,
    dp.prediction_time,
    EXTRACT(HOUR FROM dp.prediction_time) as hour_of_day
FROM demand_predictions dp
JOIN zones z ON dp.location_id = z.location_id
WITH DATA;

-- ========================
-- Refresh Function
-- ========================
CREATE OR REPLACE FUNCTION refresh_demand_forecasts()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW demand_forecasts;
END;
$$ LANGUAGE plpgsql;

