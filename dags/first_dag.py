from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import os
import pandas as pd
import random
import boto3

default_args = {
    'owner': 'your-name',
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}
output_dir = '/opt/airflow/tmp'
raw_file = 'raw_events.csv'
transformed_file = 'transformed_events.csv'
raw_path = os.path.join(output_dir, raw_file)
transformed_path = os.path.join(output_dir, transformed_file)
# Task 1: Generate dynamic event data
def generate_fake_data():
    events = [
        "Event1", "Event2", "Event3", "Event4", "Event5", "Event6",
        "Event7", "Event8", "Event9", "Event10"
    ]
    sample_events = random.sample(events, 5)
    data = {
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in sample_events],
        "event": sample_events,
        "score": [round(random.uniform(1, 10), 2) for _ in sample_events],
        "category": [random.choice(["Purchase", "PageView", "CartAbandon", "SignUp", "AccountDeletion"]) for _ in sample_events]
    }
    df = pd.DataFrame(data)
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(raw_path, index=False)
    print(f"[RAW] Saved to {raw_path}")

# Task 2: Transform data and save new CSV
def transform_and_save_csv():
    df = pd.read_csv(raw_path)
    # Sort by intensity descending
    df_sorted = df.sort_values(by="score", ascending=False)
    # Save transformed CSV
    df_sorted.to_csv(transformed_path, index=False)
    print(f"[TRANSFORMED] Sorted and saved to {transformed_path}")

# Task 3: Upload to S3
def upload_to_s3(**kwargs):
    run_date = kwargs['ds']
    bucket_name = 'hh-health-gorilla-dev'
    s3_key = f'airflow/events_transformed_{run_date}.csv'
    session = boto3.Session(profile_name='data-dev')
    s3 = session.client('s3')
    s3.upload_file(transformed_path, bucket_name, s3_key)
    print(f"Uploaded to s3://{bucket_name}/{s3_key}")

# DAG setup
with DAG(
    dag_id="simple_dag_upload_to_s3",
    default_args=default_args,
    description='Simulate a daily ETL flow with transformation and S3 upload',
    start_date=datetime(2025, 5, 24),
    schedule='@daily',
    catchup=False,
) as dag:
    task_generate = PythonOperator(
        task_id='generate_fake_events',
        python_callable=generate_fake_data
    )
    task_transform = PythonOperator(
        task_id='transform_and_save_csv',
        python_callable=transform_and_save_csv
    )
    task_upload = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,

    )
    # Task flow
    task_generate >> task_transform >> task_upload
