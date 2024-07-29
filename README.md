# Jobstreet Data Engineering Project
## Introduction
In this project, I developed an end-to-end data pipeline to process and load data from a dataset containing job listings scraped from Jobstreet. The core objectives for the project are as follow:
* Extract job listing data from Jobstreet dataset.
* Clean and transform the data as needed (e.g. handle missing values, convert data types).
* Load the data into Google Cloud Storage for further processing.
* Save the data into BigQuery and organize it using the Star Schema modeling approach.
* Orchestrate the data pipeline.
* Visualize the data by creating a dashboard which connects to the database in BigQuery.

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
2. The cleaned data is loaded into the BigQuery data warehouse - [dag_jobstreet_etl.py](https://github.com/BranB97/jobstreet-data-eng-project/blob/main/sql/create_dwh_tbls.sql)
3. Data from BigQuery is visualized via Looker Studio to facilitate analytics -

## Data Modeling
The data warehouse is designed using the Star Schema modeling approach (fact and dim tables).

![Jobstreet Data Modelling_2024-07-17T00_19_56 208Z](https://github.com/user-attachments/assets/b6ef2e0e-a14c-4fa8-b2d9-6a2e2c28c5d5)


## Infrastructure Setup
### Install Windows Subsystem for Linux (WSL)
1. Open PowerShell or Windows Command Prompt in administrator mode by right-clicking and selecting "Run as administrator" and then enter the wsl --install command.
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

### Create Google Cloud Project

