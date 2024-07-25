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


DROP TABLE IF EXISTS jobstreet_de_dwh.jobstreet_fact_tbl;
CREATE TABLE jobstreet_de_dwh.jobstreet_fact_tbl AS
SELECT DISTINCT  job_dim_tbl.job_id,
	       company_dim_tbl.company_id,
	       job_type_dim_tbl.job_type_id,
		   job_class_dim_tbl.job_class_id,
		   industry_dim_tbl.industry_id,
		   location_dim_tbl.location_id,
		   jobs_stg_tbl.min_salary,
           jobs_stg_tbl.max_salary,
		   jobs_stg_tbl.min_size,
		   jobs_stg_tbl.max_size
    FROM jobstreet_de_dwh.jobs_stg_tbl jobs_stg_tbl
	
	INNER JOIN jobstreet_de_dwh.job_type_dim_tbl job_type_dim_tbl 
	ON job_type_dim_tbl.job_type = jobs_stg_tbl.job_type
	
	INNER JOIN jobstreet_de_dwh.job_class_dim_tbl job_class_dim_tbl 
	ON job_class_dim_tbl.job_classification = jobs_stg_tbl.job_classification
	
	INNER JOIN jobstreet_de_dwh.industry_dim_tbl industry_dim_tbl 
	ON industry_dim_tbl.company_industry = jobs_stg_tbl.company_industry
	
	INNER JOIN jobstreet_de_dwh.location_dim_tbl location_dim_tbl 
	ON location_dim_tbl.job_location = jobs_stg_tbl.job_location
	
	INNER JOIN jobstreet_de_dwh.company_dim_tbl company_dim_tbl 
	ON company_dim_tbl.company_name = jobs_stg_tbl.company_name

	INNER JOIN jobstreet_de_dwh.job_dim_tbl job_dim_tbl 
	ON job_dim_tbl.job_description = jobs_stg_tbl.job_description
  AND job_dim_tbl.company_name = jobs_stg_tbl.company_name
	;
