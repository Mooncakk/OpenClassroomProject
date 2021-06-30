

<<<<<<< HEAD
from os import truncate
=======
>>>>>>> 628aa5c (ajout de definition)
import requests
from bs4 import BeautifulSoup
from lxml import html
import csv
from urllib.parse import urljoin



response = requests.get("http://books.toscrape.com/catalogue/join_902/index.html")
url = response.url
soup = BeautifulSoup(response.content, "lxml")


def sel(tag, num=0):
    info = soup.select(tag)
    return info[num]

image = urljoin(url, sel('img')['src'])

data = {
    'Product_page_url': url ,
    'Universal_product_code' : sel("td").text,
    'Title' : sel("h1").text,
    'Price_including_tax' : sel("td", 2).text,
    'Price_excluding_tax' : sel("td", 3).text,
    'Number_available' : sel("td", 5).text,
    'Product_description' : sel("p", 3).text,
    'Category' : sel("a", 3).text,
    'Review_rating' : sel("td", 6).text,
    'Image_url': image
}


with open('data_books.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, delimiter = '\t', fieldnames=data.keys())
    writer.writeheader()
    writer.writerow(data)

