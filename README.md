# Jobstreet Data Engineering Project
## Introduction
In this project, I developed an end-to-end data pipeline to process and load data from a dataset containing job listings scraped from Jobstreet. The core objectives for the project are as follow:
* Extract job listing data from Jobstreet dataset.
* Clean and transform the data as needed (e.g. handle missing values, convert data types).
* Load the data into Google Cloud Storage for further processing.
* Save the data into BigQuery and organize it using the Star Schema modeling approach.
* Orchestrate the data pipeline.
* Visualize the data by creating an interactable dashboard which connects to the database in BigQuery.

The following sections will elaborate upon the details on the tools and processes involved to create this pipeline.

## Table of Contents
1. [Dataset Used](#dataset-used)
2. [Tools Used](#tools-used)
3. [Data Pipeline Architecture](#data-pipeline-architecture)
4. [Data Modeling](#data-modeling)
5. [Infrastructure Setup](#infrastructure-setup)

## Dataset Used
The dataset used for this project are publicly accessible job listings scraped from Jobstreet. This is achieved by developing a script to scrape the job listings based on the keyword specified in a standard parameter file.

More info about the dataset and web scraping scripts can be found in the following links:
* Website: https://www.jobstreet.com.my/
* Data Dictionary:
* Raw Data: [jobstreet_jobs.csv](https://github.com/BranB97/jobstreet-data-eng-project/blob/main/data/jobstreet_jobs.csv)
* Web Scraping Scripts: [scrape_jobstreet.py](https://github.com/BranB97/jobstreet-data-eng-project/blob/main/job-scraper/scrape_jobstreet.py)

## Tools Used
* Language: Python, SQL
* Storage: Google Cloud Storage
* Data Warehouse: Google BigQuery
* Workflow Orchestration: Apache Airflow
* Visualisation: Looker Studio
* Libraries: Pandas, Selenium

## Data Pipeline Architecture
![Jobstreet_de_architecture drawio(2)](https://github.com/user-attachments/assets/b18cfc03-4348-49f1-8a26-b2acc9f59d71)

A walkthrough of the pipeline:
1. The ETL process is orchestrated via Airflow - [dag_jobstreet_etl.py](https://github.com/BranB97/jobstreet-data-eng-project/blob/main/dags/dag_jobstreet_etl.py)
2. The cleaned data is loaded into the BigQuery data warehouse - [create_dwh_tbls.sql](https://github.com/BranB97/jobstreet-data-eng-project/blob/main/sql/create_dwh_tbls.sql)
3. Data from BigQuery is visualized via Looker Studio to facilitate analytics - [Jobstreet_Dashboard.pdf](https://github.com/BranB97/jobstreet-data-eng-project/blob/main/Jobstreet_Dashboard.pdf)

## Data Modeling
The data warehouse is designed using the Star Schema modeling approach (fact and dim tables).

![Jobstreet Data Modelling_2024-07-17T00_19_56 208Z](https://github.com/user-attachments/assets/b6ef2e0e-a14c-4fa8-b2d9-6a2e2c28c5d5)


## Infrastructure Setup
### Install Windows Subsystem for Linux (WSL)
1. Open PowerShell or Windows Command Prompt in administrator mode by right-clicking and selecting "Run as administrator" and then enter the `wsl --install command`.
    ```powershell
     wsl --install
    ``` 
2. Once installation is complete, restart your machine.
3. After restart, the WSL can be opened by running Ubuntu. (Note: Ubuntu is installed as the default Linux distribution. If you want to change the disto, please refer [here](https://learn.microsoft.com/en-us/windows/wsl/basic-commands#install) )

   ![image](https://github.com/user-attachments/assets/2a69c2c6-f683-4db2-a330-04415d96747d)

   ![image](https://github.com/user-attachments/assets/5cd59236-42e9-4f54-834f-1e04f1ad4819)


### Install Airflow
1. Open WSL and install `apache-airflow` via pip with constraints that is compatible with `AIRFLOW_VERSION` and `PYTHON_VERSION` to ensure no incompatibility errors arise.
   ```shell
    AIRFLOW_VERSION=2.9.3
    PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
    CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
    pip install "apache-airflow[google]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
   ```
2. Set `AIRFLOW_HOME` based on your current directory.
   ```shell
    export AIRFLOW_HOME=$(pwd)
   ```
3. Setup Airflow metadata database based on `AIRFLOW_HOME`.
   ```shell
    airflow db migrate
   ```
4. Create a user account to login to Airflow UI.
   ```shell
    USERNAME=admin
    FIRSTNAME=data
    LASTNAME=engineer
    PASSWORD=<ENTER YOUR PASSWORD>
    EMAIL=<ENTER YOUR EMAIL>
    
    airflow users create --username USERNAME --firstname FIRSTNAME --lastname LASTNAME --role Admin --password PASSWORD --email EMAIL
   ```
5. Start Airflow webserver. 
   ```shell
    airflow webserver --port 8080
   ```
   ![start airflow webserver](https://github.com/user-attachments/assets/074e94b9-d84c-4ae9-ae24-9bcf709aeb21)

6. Open another WSL session and start Airflow scheduler.
   ```shell
    airflow scheduler
   ```   
   ![start airflow scheduler](https://github.com/user-attachments/assets/5de0ff43-0d53-4042-ac35-83ae957e028a)

7. Access the Airflow UI by visiting `http://localhost:8080/home` in your web browser. Use the account username and password that was created previously to login.
8. Alternatively, you can run [install.sh](https://github.com/BranB97/jobstreet-data-eng-project/blob/main/install.sh) to streamline the installation process.

### Setup Google Cloud Infrastructure
1. Open [Google Cloud](https://github.com/BranB97/jobstreet-data-eng-project/blob/main/install.sh) and create a new project.
2. Go [here](https://console.cloud.google.com/apis/library/browse) and activate the following APIs:
   * BigQuery API
   * Cloud Storage API
3. Go to BigQuery Studio and create your dataset.
4. Go to Cloud Storage and create your bucket.
5. Create a [Service Account](https://github.com/BranB97/jobstreet-data-eng-project/blob/main/install.sh) with the following roles:
   * `BigQuery Admin`
   * `Storage Admin`
6. Download the service account credentials and store the json file in the `AIRFLOW_HOME` directory. This will be used by Airflow to connect to GCP.

### Setup Airflow Connection
1. Open `http://localhost:8080/connection/list/` and add a connection.
2. Enter the following fields and then save the connection:
   * `Connection Id` - Your connection name
   * `Connection Type` -  Google Cloud
   * `Description` - Describe what your connection does
   * `Project Id` - Your GCP project ID
   * `Keyfile Path` - The path to your service account json key
   * `Scopes (comma separated)` - https://www.googleapis.com/auth/cloud-platform
   * `Number of Retries` - 2

### Setup Airflow Global Variables
1. Open `http://localhost:8080/variable/list/` and add the following variables:
   * `BASE_PATH` - `AIRFLOW_HOME` directory
   * `BUCKET_NAME` - The name of the bucket you created in GCS
   * `DATASET_ID` - The name of the dataset you created in BigQuery
   * `GOOGLE_CLOUD_CONN_ID` - The name of the Airflow connection you created to interface with GCP


## ETL Process
This section will breakdown the ETL workflow orchestration process. Each of the process is divided by their individual DAG tasks

![DAG ETL PIPELINE AIRFLOW](https://github.com/user-attachments/assets/a21e2911-51c6-4bc7-9ba1-f07bfb818f4f)

### Extract and Transform
In the `transformer` task, the job listing data is extracted from the raw CSV file that is placed inside the `DATA_PATH` which is the subdirectory of the `AIRFLOW_HOME` directory. Once the raw data is extracted, data cleaning and transformation is carried out prior to loading the data into GCS.

Here is the specific cleaning/transformation task that is involved:
* Replace certain sentences with more generic terms. e.g.  If the salary range of a certain record does not indicate salary info, it will replace with `No Info for Salary` instead.
* Split string and string-to-integer data type conversion. e.g. Salary range indicates `RM 7,000 - RM 10,000 per month`, the numbers will be split from the string and stored into min and maximum salary columns respectively.

### Load
In the `staging_in_gcs` task, the file containing the cleaned dataset is transferred and stored in GCS, specifically the bucket that was created previously.

![staging](https://github.com/user-attachments/assets/a03f9cf8-667a-4cd8-8357-9895b34170c6)

After that, the `load_in_dwh` task will begin and the cleaned data will be loaded into a staging table in BigQuery.

The process ends with the `load_fact_dim` task which will generate the fact and dim tables from the staging table.

![bigquery loaded tables](https://github.com/user-attachments/assets/db249f9c-d820-4f99-adc0-6dfbffa20626)

## Dashboard
Once the data warehouse is established, a dashboard is created via Looker Studio and connected to a customized dataset for visualization. You can view the dashboard [here](https://lookerstudio.google.com/reporting/2d07c793-705b-46a2-87a7-d62ded2b842a).

![dashboard1](https://github.com/user-attachments/assets/13859ccd-1cb1-48ed-8e59-9befa5b3379b)
![dashboard2](https://github.com/user-attachments/assets/0bedcc05-3b5d-4cde-b011-a69fae125013)
![dashboard3](https://github.com/user-attachments/assets/ef7035eb-ca97-4322-9757-28db8f653457)
![dashboard4](https://github.com/user-attachments/assets/e530fdeb-4c94-4743-91e0-230a86ed4639)
