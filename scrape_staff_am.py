from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time


url = 'https://staff.am/en'

driver = webdriver.Chrome() 
driver.get(url)

jobs_link = driver.find_element(By.CLASS_NAME, "hs_nav_link")  
jobs_link.click()

job_details = []

while True:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    job_items = soup.find_all('div', class_='right_radius_change')
    
    for job_item in job_items:
        job_title = job_item.find('p', class_='font_bold').text.strip()
        company = job_item.find('p', class_='job_list_company_title').text.strip()
        deadline = job_item.find('span', class_='formatted_date').text.strip()
        location = job_item.find('p', class_='job_location').text.strip()
        job_details.append((job_title, company, deadline, location))

    try:
        next_page = driver.find_element(By.CSS_SELECTOR, '.pagination li:last-child a')
        next_page.click()
        time.sleep(1)
    except NoSuchElementException:
        break
    
driver.quit()


df = pd.DataFrame(job_details, columns=['Job title', 'Company', 'Deadline', 'Location'])
df.to_csv('job_details.csv', index=False)
print("Data successfully saved to 'job_details.csv'.")