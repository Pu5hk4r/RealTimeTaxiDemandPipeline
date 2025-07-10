from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from storage.init_db import initialize_database
from ml_model.train_model import train_and_save_model
from ml_model.predict_demand import DemandPredictor

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'taxi_demand_pipeline',
    default_args=default_args,
    description='Taxi demand prediction pipeline',
    schedule_interval='@daily',  # Change to @hourly or cron
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

init_db = PythonOperator(
    task_id='init_database',
    python_callable=initialize_database,
    dag=dag,
)

ingest_data = BashOperator(
    task_id='kafka_ingest',
    bash_command='python /app/data_ingestion/kafka_producer.py',
    dag=dag,
)

spark_process = BashOperator(
    task_id='run_spark_processing',
    bash_command='spark-submit --master local /app/data_processing/spark_transform.py',
    dag=dag,
)

train_model = PythonOperator(
    task_id='train_model',
    python_callable=train_and_save_model,
    dag=dag,
)

def run_prediction():
    predictor = DemandPredictor()
    predictor.run(publish_to_kafka=False)

predict_demand = PythonOperator(
    task_id='predict_demand',
    python_callable=run_prediction,
    dag=dag,
)

init_db >> ingest_data >> spark_process >> train_model >> predict_demand

