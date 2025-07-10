
<p align="center">
  <img src="https://img.icons8.com/external-flaticons-lineal-color-flat-icons/64/000000/external-taxi-transportation-flaticons-lineal-color-flat-icons.png" width="60"/>
</p>

<h1 align="center">🚖 NYC Taxi Demand Prediction Pipeline</h1>

<p align="center">
  Real-time machine learning pipeline for predicting zone-wise taxi demand in NYC using <b>Kafka</b>, <b>Spark</b>, <b>PostgreSQL</b>, and <b>Streamlit</b>.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white"/>
  <img src="https://img.shields.io/badge/Apache_Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
</p>

---

## 🌟 Overview

> A full-stack real-time data pipeline for **predicting taxi demand across NYC** neighborhoods.  
> Designed for live ingestion and historical replay, it helps visualize traffic hot zones and optimize fleet allocation.
> Automatic Orchestrate By Airflow Train model and predict at particular timr interval.

![model1](https://github.com/Pu5hk4r/taxi-demand-pipeline/blob/main/assets/model1.png)
![model2](https://github.com/Pu5hk4r/taxi-demand-pipeline/blob/main/assets/model2.png)
![model3](https://github.com/Pu5hk4r/taxi-demand-pipeline/blob/main/assets/model3.png)

---

## 📌 Table of Contents

- [🧠 Project Motivation](#-project-motivation)
- [🛠️ Tools & Technologies](#️-tools--technologies)
- [📐 System Architecture](#-system-architecture)
- [📂 Folder Structure](#-folder-structure)
- [🔁 Data Flow Pipeline](#-data-flow-pipeline)
- [🧪 ML Model Details](#-ml-model-details)
- [📊 Live Dashboard](#-live-dashboard)
- [🗄️ PostgreSQL Schema](#️-postgresql-schema)
- [🚀 Getting Started](#-getting-started)
- [🎯 Future Enhancements](#-future-enhancements)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## 🧠 Project Motivation

Urban areas suffer from:
- ⏱️ Passenger wait times
- 🚖 Idle driver time
- 💸 Resource wastage

This project helps:
- 🧭 Predict demand hotzones
- 🚦 Optimize driver allocation
- 🔍 Enable smarter transport systems

---

## 🛠️ Tools & Technologies

| Layer        | Tool                      | Purpose                                      |
|--------------|----------------------------|----------------------------------------------|
| Ingestion    | Kafka                      | Real-time data transport                     |
| Processing   | Spark Structured Streaming | ETL, windowing, transformations              |
| ML           | scikit-learn               | Demand prediction using Random Forest        |
| Storage      | PostgreSQL                 | Store predictions                            |
| Dashboard    | Streamlit                  | Visual live updates                          |
| Orchestration| Airflow (MWAA)             | DAG scheduling (optional)                    |

---

## 📐 System Architecture

![architecture](https://github.com/Pu5hk4r/taxi-demand-pipeline/blob/main/assets/PushkarProjectArchitecture.png)


graph TD
    A[Kafka Producer - NYC Taxi Trips] --> B[Kafka Topic: taxi_data]
    B --> C[Spark Structured Streaming]
    C --> D[Feature Engineering and Aggregation]
    D --> E["Trained ML Model - Random Forest"]
    E --> F[Kafka Topic: demand_prediction]
    F --> G1[Streamlit Dashboard]
    F --> G2[PostgreSQL Storage]

---
## 📂 Folder Structure

<pre><code>📦 taxi-demand-prediction/ 

  taxi-demand-pipeline/
├── kafka/                 # Kafka producer
│   └── producer.py
├── spark/                 # PySpark streaming + transform
│   └── streaming_job.py
├── models/                # Trained ML models (pkl/joblib)
│   └── demand_model.pkl
├── airflow/               # DAGs for retraining/refresh
│   └── taxi_dag.py
├── fastapi_app/           # Prediction API
│   ├── main.py
│   └── predict.py
├── streamlit_dashboard/   # Visualization UI
│   └── app.py
├── postgres/              # DB schema + queries
│   └── schema.sql
├── docker/                # Docker Compose, Dockerfiles
│   └── docker-compose.yml
├── data/                  # Sample CSV/JSON for local testing
├── README.md
└── .env

 </code></pre>



## 🔁 Data Flow Pipeline

🟢 Kafka Producer streams data.

🔶 Spark Streaming consumes and processes it.

🧮 Feature Engineering on Spark.

🤖 ML Model predicts demand.

📣 Predictions go to Kafka topic.

📊 Streamlit shows demand.

🗃️ PostgreSQL stores for analysis.

---

## 🧪 ML Model Details
Model: Random Forest Regressor

Framework: Scikit-learn

Features: Hour, Weekday, Zones, Distance, Passenger Count

Training Source: .parquet files

Metrics:

R²: 0.91

RMSE: 2.65

---

## 📊 Live Dashboard
Built using Streamlit, with:

🗺️ NYC zone-wise demand map

🔄 Auto-updates via Kafka

🔢 Table + Graph modes

🎨 Color-coded predictions:

🟢 Low

🟡 Medium

🔴 High

---
## 🗄️ PostgreSQL Schema
sql
<pre><code>
  CREATE TABLE taxi_demand_prediction (
    id SERIAL PRIMARY KEY,
    zone_id INT,
    prediction_time TIMESTAMP,
    predicted_demand INT,
    model_version VARCHAR(50)
);

  
</code></pre>


---

## 🚀 Getting Started
## ✅ Step 1: Start Docker with Kafka + PGAdmin

<pre><code>
docker-compose -f docker/docker-compose.yml up -d
docker ps
</code></pre>
---
## ✅ Step 2: Prepare Database

<pre><code>
 psql -U postgres -c "CREATE DATABASE taxi_demand;"
psql -U postgres -d taxi_demand -f storage/schema.sql
psql -U postgres -d taxi_demand -f storage/sample_raw_trips.sql
</code></pre>
---

## ✅ Step 3: Process Data & Train Model

<pre><code>
python -m data_processing.spark_transform
python -m data_ingestion.kafka_producer
python -m ml_model.train_model
python -m ml_model.predict_demand

</code></pre>
---
## ✅ Step 4: Create Kafka Topics

<pre><code>
docker exec -it kafka kafka-topics --create --topic taxi_trips --bootstrap-server localhost:29092 --partitions 1 --replication-factor 1
docker exec -it kafka kafka-topics --create --topic taxi_zones --bootstrap-server localhost:29092 --partitions 1 --replication-factor 1
docker exec -it kafka kafka-topics --create --topic taxi_predictions --bootstrap-server localhost:29092 --partitions 1 --replication-factor 1

</code></pre>
---

## 🎯 Future Enhancements
🌦️ Add weather/traffic input

📦 Schema Registry + Kafka Connect

⚙️ MLflow-based model tracking

🧊 Dockerized CI/CD deployment

🔔 Spike alerts in Streamlit

---

## 🤝 Contributing
Fork the repo

Create a branch

Submit a PR

Add your name to contributors 🙌

---

## 📜 License
MIT License. See LICENSE.

<p align="center"> Built with ❤️ by <strong>Pushkar Sharma</strong> </p> ```













