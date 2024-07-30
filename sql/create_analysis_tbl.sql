CREATE OR REPLACE TABLE jobstreet_de_dwh.analysis_tbl AS
SELECT   jobstreet_fact_tbl.job_id,
	       jobstreet_fact_tbl.company_id,
				 job_dim_tbl.job_description,
				 job_dim_tbl.job_salary,
				 company_dim_tbl.company_name,
				 company_dim_tbl.company_benefits,
				 case
				   when company_dim_tbl.company_review = 'No info for Company Review'
					 then null
					 else cast(company_dim_tbl.company_review as FLOAT64)
				 end review_score,
				 company_dim_tbl.company_size,
	       job_type_dim_tbl.job_type,
		     job_class_dim_tbl.job_classification,
		     industry_dim_tbl.company_industry,
		   location_dim_tbl.job_location,
		   jobstreet_fact_tbl.min_salary,
           jobstreet_fact_tbl.max_salary,
		   jobstreet_fact_tbl.min_size,
		   jobstreet_fact_tbl.max_size
    FROM jobstreet_de_dwh.jobstreet_fact_tbl jobstreet_fact_tbl
	
	INNER JOIN jobstreet_de_dwh.job_type_dim_tbl job_type_dim_tbl 
	ON job_type_dim_tbl.job_type_id = jobstreet_fact_tbl.job_type_id
	
	INNER JOIN jobstreet_de_dwh.job_class_dim_tbl job_class_dim_tbl 
	ON job_class_dim_tbl.job_class_id = jobstreet_fact_tbl.job_class_id
	
	INNER JOIN jobstreet_de_dwh.industry_dim_tbl industry_dim_tbl 
	ON industry_dim_tbl.industry_id = jobstreet_fact_tbl.industry_id
	
	INNER JOIN jobstreet_de_dwh.location_dim_tbl location_dim_tbl 
	ON location_dim_tbl.location_id = jobstreet_fact_tbl.location_id
	
	INNER JOIN jobstreet_de_dwh.company_dim_tbl company_dim_tbl 
	ON company_dim_tbl.company_id = jobstreet_fact_tbl.company_id

	INNER JOIN jobstreet_de_dwh.job_dim_tbl job_dim_tbl 
	ON job_dim_tbl.job_id = jobstreet_fact_tbl.job_id

	order by job_id, company_id
	;
