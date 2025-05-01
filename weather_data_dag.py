#!/usr/bin/env python3

"""
Airflow DAG to automate the weather data processing workflow.
This DAG includes tasks for data collection and preprocessing.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import os

# Import our custom scripts
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from collect_data import collect_data
from preprocess_data import preprocess_data
from version_data import version_with_dvc

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'weather_data_processing',
    default_args=default_args,
    description='A DAG to process weather data',
    schedule_interval=timedelta(days=1),  # Run daily
    start_date=datetime(2025, 5, 1),
    catchup=False,
    tags=['weather', 'data_processing'],
)

# Define file paths with timestamp to avoid overwriting
timestamp = "{{ ts_nodash }}"
raw_data_path = 'raw_data.csv'
collected_data_path = f'collected_data_{timestamp}.csv'
processed_data_path = f'processed_data_{timestamp}.csv'

# Task 1: Collect Data
collect_task = PythonOperator(
    task_id='collect_data',
    python_callable=collect_data,
    op_kwargs={
        'source_file': raw_data_path,
        'target_file': collected_data_path
    },
    dag=dag,
)

# Task 2: Preprocess Data
preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    op_kwargs={
        'input_file': collected_data_path,
        'output_file': processed_data_path
    },
    dag=dag,
)

# Task 3: Version Data with DVC
version_task = PythonOperator(
    task_id='version_data',
    python_callable=version_with_dvc,
    op_kwargs={
        'data_file': processed_data_path
    },
    dag=dag,
)

# Task 4: Create a latest symlink to the most recent processed data
symlink_task = BashOperator(
    task_id='create_latest_symlink',
    bash_command=f'ln -sf {processed_data_path} processed_data_latest.csv',
    dag=dag,
)

# Define task dependencies
collect_task >> preprocess_task >> version_task >> symlink_task