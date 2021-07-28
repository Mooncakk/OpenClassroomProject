
import requests
from bs4 import BeautifulSoup
from lxml import html
import csv
from urllib.parse import urljoin

url = 'http://books.toscrape.com/catalogue/join_902/index.html'

def get_page(url):
#Contenu de la page web
    response = requests.get(url)
    return BeautifulSoup(response.content, 'lxml')

def sel(lien, tag, num=0):
    info = get_page(lien).select(tag)
    return info[num]


def get_book_data():
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
    return data

def get_book_name():
  #Récupère le nom de la catégorie
  book_name = get_page(url).select_one('div > h1')
  return book_name.text

def create_csv_file():
    #Créer le fichier CSV
    book_data = get_book_data()
    headlines = book_data.keys()
    book = get_book_name()
    with open(book + '.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter = ';', fieldnames=headlines)
        writer.writeheader()
        writer.writerow(book_data)

#create_csv_file()

