INSERT INTO raw_trips (
    vendor_id, tpep_pickup_datetime, tpep_dropoff_datetime, passenger_count, trip_distance, pu_location_id, do_location_id, fare_amount
) VALUES
(1, '2025-07-01 08:00:00', '2025-07-01 08:15:00', 1, 2.5, 101, 202, 15.0),
(2, '2025-07-01 09:00:00', '2025-07-01 09:25:00', 2, 5.0, 102, 203, 25.0),
(1, '2025-07-01 10:00:00', '2025-07-01 10:10:00', 1, 1.2, 101, 204, 10.0),
(2, '2025-07-01 11:00:00', '2025-07-01 11:30:00', 3, 7.8, 103, 205, 35.0);
