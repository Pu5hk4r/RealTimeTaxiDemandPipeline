from pyspark.sql import SparkSession
from pyspark.sql.functions import hour, dayofweek, col
from utils.helpers import save_processed_data
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    spark = SparkSession.builder \
    .appName("TaxiDemandTransform") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()


    # Read raw Parquet file
    df = spark.read.parquet("data/raw/yellow_tripdata_2025-01.parquet")

    # Rename column and compute hour/day, then aggregate
    df = df.withColumn("pickup_hour", hour("tpep_pickup_datetime")) \
       .withColumn("pickup_day_of_week", dayofweek("tpep_pickup_datetime")) \
       .groupBy("PULocationID", "pickup_hour", "pickup_day_of_week") \
       .count() \
       .withColumnRenamed("count", "pickup_count") \
       .withColumnRenamed("PULocationID", "pu_location_id")


    # Convert to Pandas and save
    df_pd = df.toPandas()
    save_processed_data(df_pd, "pickup_counts.parquet")

    logger.info("✅ Saved transformed pickup data.")

if __name__ == "__main__":
    main()
