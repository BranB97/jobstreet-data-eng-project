import os
from std_para import BASE_URL, GECKODRIVER_PATH, KEYWORDS, LOG_DIR, DATA_DIR, LOG_INFO_PATH, LOG_INFO_FILEMODE, MAX_PAGE, FIREFOX_PATH


from pathlib import Path
Path(LOG_DIR).mkdir(exist_ok=True)

import logging
logging.basicConfig(level=logging.INFO, filename=LOG_INFO_PATH, filemode=LOG_INFO_FILEMODE)

import pandas as pd


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

options = Options()
options.add_argument("--headless=new")
options.binary_location = FIREFOX_PATH
service = Service(executable_path=GECKODRIVER_PATH)



class scrape_jobstreet(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.browser = webdriver.Firefox(options=options, service=service)
        self.col_company_name = []
        self.col_job_salary = []
        self.col_company_review = []
        self.col_company_size = []
        self.col_company_industry = []
        self.col_job_description = []
        self.col_job_type = []
        self.col_job_location = []
        self.col_company_benefits = []
        self.col_job_classification = []
        
    def start_scrapping(self):
        #Loop through the keywords defined in the std_para and use it as the input to begin search
        for find_keyword in KEYWORDS:
            self.browser.get(BASE_URL)
            WebDriverWait(self.browser,10).until(
                ec.element_to_be_clickable((By.XPATH, "//*[@id='keywords-input']"))).send_keys(find_keyword)

            searchkw_elem = self.browser.find_element(By.XPATH, "//*[@id='keywords-input']")
            searchkw_elem.send_keys(Keys.ENTER)

            WebDriverWait(self.browser, 10).until(
                ec.presence_of_all_elements_located((By.XPATH, "//article[@data-automation='normalJob']")))

            #Loop through the pages for scraping data. The range (MAX_PAGE) is set in the std_para
            for page in range(1, MAX_PAGE+1):
                current_job_url = self.browser.current_url
                self.logger.info(f"Current Page: {current_job_url}")
                WebDriverWait(self.browser, 10).until(
                    ec.presence_of_all_elements_located((By.XPATH, "//article[@data-automation='normalJob']")))
                article_elems = self.browser.find_elements(By.XPATH, '//article')

                self.logger.info(f"No of job cards: {len(article_elems)}")

                for article_elem in article_elems:
                  self.browser.execute_script("arguments[0].scrollIntoView(true)", article_elem)
                  self.browser.execute_script("arguments[0].click()", article_elem)

                  WebDriverWait(self.browser, 10).until(
                      ec.presence_of_all_elements_located((By.XPATH, "//div[@data-automation='splitViewJobDetailsWrapper']")))
                  
                  self.scrape_data()
                next_page_link = self.browser.find_element(By.CSS_SELECTOR, "li._4cz756a6 > a")
                self.browser.execute_script("arguments[0].click()", next_page_link)

        self.logger.info('Scrapping process done!')

        #Organize the data using pandas dataframe
        df = pd.DataFrame(
            {
                "company_name": self.col_company_name,
                "job_description": self.col_job_description,
                "job_salary": self.col_job_salary,
                "job_type": self.col_job_type,
                "job_classification": self.col_job_classification,
                "company_review": self.col_company_review,
                "company_benefits": self.col_company_benefits,
                "company_size": self.col_company_size,
                "company_industry": self.col_company_industry,
                "job_location": self.col_job_location
            }
            
            )
            

        df.to_csv(f"{DATA_DIR}\\jobstreet_jobs.csv", index=False, encoding="utf-8")

    def scrape_data(self):
        WebDriverWait(self.browser, 10).until(
                    ec.presence_of_all_elements_located((By.XPATH, "//div[@data-automation='jobDetailsPage']")))

        company_name_elem = self.browser.find_element(By.XPATH, "//*[@data-automation='advertiser-name']")
        company_name_text = company_name_elem.text
        self.col_company_name.append(company_name_text)
        self.logger.info(f"Scraping Company Name: {company_name_text}")

        job_desc_elem = self.browser.find_element(By.XPATH, "//*[@data-automation='job-detail-title']")
        job_desc_text = job_desc_elem.text
        self.col_job_description.append(job_desc_text)


        job_location_elem = self.browser.find_element(By.XPATH, "//*[@data-automation='job-detail-location']")
        job_location_text = job_location_elem.text
        self.col_job_location.append(job_location_text)


        job_type_elem = self.browser.find_element(By.XPATH, "//*[@data-automation='job-detail-work-type']")
        job_type_text = job_type_elem.text
        self.col_job_type.append(job_type_text)


        job_class_elem = self.browser.find_element(By.XPATH, "//*[@data-automation='job-detail-classifications']")
        job_class_text = job_class_elem.text
        self.col_job_classification.append(job_class_text)


        job_salary_text = self.additional_info(selector = "//*[@data-automation='job-detail-salary']", text = "Job Salary")
        self.col_job_salary.append(job_salary_text)



        company_review_text = self.additional_info(selector = "//*[@data-automation='company-review']", text = "Company Review")
        self.col_company_review.append(company_review_text)


        company_benefits_text = self.additional_info_css(selector = "div._4cz75696 > div:nth-child(2) > section:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div", text = "Company Benefits")
        self.col_company_benefits.append(company_benefits_text)


        company_size_text = self.additional_info_css(selector = "div._4cz75696 > div:nth-child(1) > div:nth-child(2) > section:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1) > span", text = "Company Size")
        self.col_company_size.append(company_size_text)


        company_industry_text = self.additional_info_css(selector = "div._4cz75696 > div:nth-child(1) > div:nth-child(2) > section:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span", text = "Company Industry")
        self.col_company_industry.append(company_industry_text)


        

    #to scrape optional info in the job listing - e.g company size, benefits, industry etc.
    def additional_info(self, selector, text):
        try:
            add_info_elem = self.browser.find_element(By.XPATH, selector)
            add_info_text = add_info_elem.text
        except NoSuchElementException:
            add_info_text = f"No info for {text}"

        return add_info_text

    #scraping additional info via css instead - a workaround method when the usual method does not work.
    def additional_info_css(self, selector, text):
        try:
            add_info_elem = self.browser.find_element(By.CSS_SELECTOR, selector)
            add_info_text = add_info_elem.text
        except NoSuchElementException:
            add_info_text = f"No info for {text}"

        return add_info_text

        
        

if __name__ == "__main__":
    jobscrape = scrape_jobstreet()
    jobscrape.start_scrapping()
