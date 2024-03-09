import requests
from bs4 import BeautifulSoup
import re


def scrape_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        names = [name.text.strip() for name in soup.find_all('a', class_='title')]
        prices = [price.text.strip() for price in soup.find_all(class_=re.compile(r'.*price.*'))]
        reviews = [review.text.strip() for review in soup.find_all(class_=re.compile(r'.*review.*'))]
       
        for name, price, review in zip(names, prices, reviews):
            print("Name:", name)
            print("Price:", price)
            print("Review:", review)
            print()

        with open("data.txt", "w") as file:
            for name, price, review in zip(names, prices, reviews):
                file.write(f"Name: {name}\nPrice: {price}\nReview: {review}\n\n")

        print("Data saved in text file.")

    except requests.exceptions.RequestException as e:
        print("Error:", e)

 
url = "https://webscraper.io/test-sites/e-commerce/allinone"
scrape_details(url)