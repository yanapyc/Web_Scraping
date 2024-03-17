import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        names = [name.text.strip() for name in soup.find_all('a', class_='title')]
        prices = [price.text.strip() for price in soup.find_all('h4', class_='float-end price card-title pull-right')]
        descriptions = [description.text.strip() for description in soup.find_all('p', class_="description")]
        reviews = [review.text.strip() for review in soup.find_all('p', "float-end review-count")]
        
        return names, prices, descriptions, reviews

    except requests.exceptions.RequestException as e:
        print("Error:", e)

def scraping_with_selenium(url):
    driver = webdriver.Chrome()
    driver.get(url)

    menu_items = driver.find_element(By.ID, 'side-menu').find_elements(By.CLASS_NAME, 'nav-item')

    for item in menu_items[1:]:
        item.click()
        products = driver.find_element(By.CSS_SELECTOR, '.sidebar').find_element(By.CSS_SELECTOR, '.active').find_elements(By.CLASS_NAME, 'nav-item')

        for product in products:
            product.click()
            soup = scrape_details(driver.current_url)

            with open('scraping_with_selenium.txt', 'a') as file:
                names, prices, descriptions, reviews = soup
                for name, price, description, review in zip(names, prices, descriptions, reviews):
                    file.write("Name: " + name + "\n")
                    file.write("Price: " + price + "\n")
                    file.write("Review: " + review + "\n")
                    file.write("Description: " + description + "\n")
                    file.write("----------------------\n")
            
            driver.back()
        driver.back()
    driver.quit()

url = "https://webscraper.io/test-sites/e-commerce/allinone"
scraping_with_selenium(url)
