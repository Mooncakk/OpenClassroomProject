

import requests
from bs4 import BeautifulSoup
from lxml import html
from urllib.parse import urljoin
import math
import csv


url = 'https://books.toscrape.com/catalogue/category/books/religion_12/index.html'



def get_page(url):
#Contenu de la page web
    response = requests.get(url)
    return BeautifulSoup(response.content, 'lxml')


books_links = []

def get_books_links(url = url):
#Récupère les liens des livres d'une page et les stock dans une liste --> books_links
    articles = get_page(url).select('h3')
    for tag in articles:
        a = tag.select_one('a')
        link = urljoin (url, a['href'])
        books_links.append(link)
        


def get_category_name():
  #Récupère le nom de la catégorie
  category = get_page(url).select_one('.page-header > h1')
  return category.text

def get_page_number(a=0):
  #Calculer le nombre de page d'une catégorie
  nb_livres = get_page(url).select_one('form > strong')
  nb_pages = math.ceil(int(nb_livres.text) / 20)
  return nb_pages + a


def pagination(): 
# Boucle qui recupère le lien de la page suivante et éxecute la fonction qui récupère les URL des livres d'une page
  get_books_links()
  if get_page_number() > 1:
    for page_number in range(2,get_page_number(1)):
      
      next_page_url = urljoin(url,'page-'+ str(page_number)+'.html')
      
      get_books_links(next_page_url)
  else:
    return
  return


def sel(lien, tag, num=0):
    #Fonction qui execute notre soup
    info = get_page(lien).select(tag)
    return info[num]


def get_book_data(book_link):
  #Extrait les infos du livre
  image = urljoin(book_link, sel(book_link,'.item > img')['src'])  
  data = (
    book_link,
    sel(book_link,"td").text,
    sel(book_link,"h1").text,
    sel(book_link,"td", 2).text,
    sel(book_link,"td", 3).text,
    sel(book_link,"td", 5).text,
    sel(book_link,"p", 3).text,
    sel(book_link,"a", 3).text,
    sel(book_link,"td", 6).text,
    image
        )
  return data
  
def csv_headlines():
  #Éléments de l'entête du fichier CSV
  headlines = (
    'Product_page_url',
    'Universal_product_code',
    'Title',
    'Price_including_tax',
    'Price_excluding_tax',
    'Number_available',
    'Product_description',
    'Category',
    'Review_rating',
    'Image_url'
        )
  return headlines

def csv_file_headlines():
  #Création de l'entête du fichier CSV
  category_name = get_category_name()
  headlines = csv_headlines()
  with open('Category_' + category_name + '_Books.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, delimiter = ';', fieldnames=headlines)
    writer.writeheader()
    

def csv_file_creation(l):
  #Création du fichier csv au nom de la catégorie
  category_name = get_category_name()
  headlines = csv_headlines()
  book_data = get_book_data(l)
  with open('Category_' + category_name + '_Books.csv', 'a+') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(book_data)
    
 

def extract_to_csv():
  #Boucle sur les URL stocké dans une liste, y extrait les donnnées et crée le fichier CSV
  csv_file_headlines()
  for i in books_links:
    csv_file_creation(i)
  return


def main():
  #Exécute les fonctions du script
  pagination()
  extract_to_csv()


main()
