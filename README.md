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
1. [Dataset Used](https://github.com/BranB97/jobstreet-data-eng-project?tab=readme-ov-file#dataset-used)
2. 

## Dataset Used
The dataset used for this project are publicly accessible job listings scraped from Jobstreet. This is achieved by developing a script to scrape the job listings based on the keyword specified in a standard parameter file.

More info about the dataset and web scraping scripts can be found in the following links:
* Website:
* Data Dictionary:
* Raw Data:
* Web Scraping Scripts:

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
1. The ETL process is orchestrated via Airflow - 
2. The cleaned data is loaded into the BigQuery data warehouse -
3. Data is visualized to facilitate analytics -

## Infrastructure Setup
### Install Airflow


