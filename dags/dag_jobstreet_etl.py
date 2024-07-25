import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import pandas as pd

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.decorators import task
from airflow.utils.dates import days_ago
from airflow.models.variable import Variable
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from uuid import uuid4

#Global Variables - Airflow and GCP settings, directories, etc. 
DATASET_ID = Variable.get("DATASET_ID")
BASE_PATH = Variable.get("BASE_PATH")
BUCKET_NAME = Variable.get("BUCKET_NAME")
GOOGLE_CLOUD_CONN_ID = Variable.get("GOOGLE_CLOUD_CONN_ID")
BIGQUERY_TABLE_NAME = "jobs_stg_tbl"
GCS_OBJECT_NAME = "et_job_data.csv"
DATA_PATH = f"{BASE_PATH}/data"
OUT_PATH = f"{DATA_PATH}/{GCS_OBJECT_NAME}"


default_args = {
    'owner': 'admin',
    'concurrency': 1,
    'retries': 0
    }

with DAG(
    "dag_jobstreet_etl",
    default_args = default_args,
    description = "ETL Pipeline for JobStreet Job Listing",
    start_date =days_ago(1),
    tags=['excel', 'csv', 'jobstreet'],
    template_searchpath = f"{BASE_PATH}/sql"
    ) as dag:

    #transform the data in the raw source file
    @task()
    def transformer():
        df = pd.read_csv(f"{DATA_PATH}/jobstreet_jobs.csv")
        df['id'] = df.apply(lambda x: uuid4(), axis=1)
        df["job_salary"] = df["job_salary"].apply(lambda x: "No info for Job Salary" if x == "Add expected salary to your profile for insights" else x)
        df["min_salary"] = df["job_salary"].apply(lambda x: extract_salary(x, 0) if x != "No info for Job Salary" else None)
        df["max_salary"] = df["job_salary"].apply(lambda x: extract_salary(x, 1) if x != "No info for Job Salary" else None)
        df["min_size"] = df["company_size"].apply(lambda x: extract_size(x, 0) if x != "No info for Company Size" else None)
        df["max_size"] = df["company_size"].apply(lambda x: extract_size(x, 1) if x != "No info for Company Size" else None)
        df["company_review"] = df["company_review"].apply(lambda x: "No info for company review" if x == "View all jobs" else x)
        new_cols = ["id", "company_name", "job_description", "job_salary", "job_type", "job_classification", "company_review", "company_benefits", "company_size", "company_industry", "job_location", "min_salary", "max_salary"
                    , "min_size", "max_size"]
        df = df.reindex(columns = new_cols)

        df.to_csv(OUT_PATH, index=False)


    def extract_salary(salary_range, position):
        try:
            salary = salary_range.replace("RM", "").replace("$", "").replace("MYR", "").replace(" ", "").replace("k", "000").replace("permonth", "").replace("peryear", "").replace("perhour", "").replace("p.m.", "").replace("p.a.", "").split("-")
            return salary[position]
        except (ValueError, IndexError):
            return None

    def extract_size(size_range, position):
        try:
            size = size_range.replace(" ", "").replace("Morethan", "").replace("employees", "").split("-")
            return size[position]
        except (ValueError, IndexError):
            return None
    
    #load the cleaned data in a staging directory - GCS
    staging_in_gcs = LocalFilesystemToGCSOperator(
        task_id = "staging_in_gcs",
        gcp_conn_id = GOOGLE_CLOUD_CONN_ID,
        src = OUT_PATH,
        dst = GCS_OBJECT_NAME,
        bucket = BUCKET_NAME
        )

    #load the data in BigQuery database
    load_in_dwh = GCSToBigQueryOperator(
        task_id = "load_in_dwh",
        gcp_conn_id = GOOGLE_CLOUD_CONN_ID,
        bucket = BUCKET_NAME,
        source_objects = [GCS_OBJECT_NAME],
        destination_project_dataset_table = f"{DATASET_ID}.{BIGQUERY_TABLE_NAME}",
        schema_fields = [
            {"name": "id", "type": "STRING", "mode": "REQUIRED"},
            {"name": "company_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "job_description", "type": "STRING", "mode": "NULLABLE"},
            {"name": "job_salary", "type": "STRING", "mode": "NULLABLE"},
            {"name": "job_type", "type": "STRING", "mode": "NULLABLE"},
            {"name": "job_classification", "type": "STRING", "mode": "NULLABLE"},
            {"name": "company_review", "type": "STRING", "mode": "NULLABLE"},
            {"name": "company_benefits", "type": "STRING", "mode": "NULLABLE"},
            {"name": "company_size", "type": "STRING", "mode": "NULLABLE"},
            {"name": "company_industry", "type": "STRING", "mode": "NULLABLE"},
            {"name": "job_location", "type": "STRING", "mode": "NULLABLE"},
            {"name": "min_salary", "type": "FLOAT64", "mode": "NULLABLE"},
            {"name": "max_salary", "type": "FLOAT64", "mode": "NULLABLE"},
            {"name": "min_size", "type": "INT64", "mode": "NULLABLE"},
            {"name": "max_size", "type": "INT64", "mode": "NULLABLE"},
            ],
        autodetect = False,
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        field_delimiter=",",
        write_disposition = "WRITE_TRUNCATE"
        )

    #organize the data into fact and dim tables
    load_fact_dim = BigQueryInsertJobOperator(
        task_id="load_fact_dim",
        configuration={
        "query": {
            "query": "{% include 'create_dwh_tbls.sql' %}",                          
            "useLegacySql": False
            }
        },
        gcp_conn_id = GOOGLE_CLOUD_CONN_ID
        )

    #dummy operators to act as 'bookends' to the workflow
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    extract_transform = transformer()

    start >> extract_transform >> staging_in_gcs >> load_in_dwh >> load_fact_dim >> end
