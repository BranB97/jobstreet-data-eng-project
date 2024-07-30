DROP TABLE IF EXISTS jobstreet_de_dwh.industry_dim_tbl;
CREATE TABLE jobstreet_de_dwh.industry_dim_tbl AS
	SELECT ROW_NUMBER() OVER (ORDER BY company_industry) as industry_id, 
               company_industry
         FROM jobstreet_de_dwh.jobs_stg_tbl
         GROUP BY company_industry;

DROP TABLE IF EXISTS jobstreet_de_dwh.job_type_dim_tbl;
CREATE TABLE jobstreet_de_dwh.job_type_dim_tbl AS
	SELECT ROW_NUMBER() OVER (ORDER BY job_type) as job_type_id, 
               job_type
         FROM jobstreet_de_dwh.jobs_stg_tbl
         GROUP BY job_type;

DROP TABLE IF EXISTS jobstreet_de_dwh.job_class_dim_tbl;
CREATE TABLE jobstreet_de_dwh.job_class_dim_tbl AS
        SELECT ROW_NUMBER() OVER (ORDER BY job_classification) as job_class_id, 
               job_classification
         FROM jobstreet_de_dwh.jobs_stg_tbl
         GROUP BY job_classification;

DROP TABLE IF EXISTS jobstreet_de_dwh.location_dim_tbl;
CREATE TABLE jobstreet_de_dwh.location_dim_tbl AS		 
		 SELECT ROW_NUMBER() OVER (ORDER BY job_location) as location_id, 
		        job_location
         FROM jobstreet_de_dwh.jobs_stg_tbl
         GROUP BY job_location;

DROP TABLE IF EXISTS jobstreet_de_dwh.job_dim_tbl;
  CREATE TABLE jobstreet_de_dwh.job_dim_tbl AS
	SELECT ROW_NUMBER() OVER (ORDER BY job_description) as job_id,
	       job_description,
         company_name,
           job_salary,
           min_salary,
           max_salary
         FROM jobstreet_de_dwh.jobs_stg_tbl
         GROUP BY job_description, company_name, job_salary, min_salary, max_salary;

DROP TABLE IF EXISTS jobstreet_de_dwh.company_dim_tbl;		 
CREATE TABLE jobstreet_de_dwh.company_dim_tbl AS
	SELECT ROW_NUMBER() OVER (ORDER BY company_name) as company_id,
           company_name,
           company_review,
           company_benefits,
           company_size,
           min_size,
           max_size,
         FROM jobstreet_de_dwh.jobs_stg_tbl
         GROUP BY company_name, company_review, company_benefits, company_size, min_size, max_size;
