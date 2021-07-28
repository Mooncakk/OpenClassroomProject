
import requests
from bs4 import BeautifulSoup
from lxml import html
from urllib.parse import urljoin
import math
import csv


url = 'http://books.toscrape.com/index.html'


def get_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'lxml')

books_category_links = []

def get_books_category_links():
    #Récuperer le lien des livres de chaque catégorie
    get_category = get_page(url).select_one('.nav > li > ul')
    for i in range (50):
        a = get_category.select('a')[i]
        link = urljoin(url, a['href'])
        books_category_links.append(link)

def get_category_name(category_link):
  #Récupère le nom de la catégorie
  category = get_page(category_link).select_one('.page-header > h1')
  return category.text

def get_page_number(category_link, a=0):
  #Calculer le nombre de page d'une catégorie
  nb_livres = get_page(category_link).select_one('form > strong')
  nb_pages = math.ceil(int(nb_livres.text) / 20)
  return nb_pages + a

books_links = []

def get_books_links(category_link):
#Récupère les liens des livres d'une page et les stock dans une liste --> books_links
    articles = get_page(category_link).select('h3')
    for tag in articles:
        a = tag.select_one('a')
        link = urljoin (category_link, a['href'])
        books_links.append(link)


def pagination(category_link): 
# Boucle qui recupère le lien de la page suivante et éxecute la fonction qui récupère les URL des livres d'une page
  get_books_links(category_link)
  if get_page_number(category_link) > 1:
    for page_number in range(2,get_page_number(category_link,1)):
      
        next_page_url = urljoin(category_link,'page-'+ str(page_number)+'.html')
        get_books_links(next_page_url)
  else:
    return
  return


def sel(lien, tag, num = 0):
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



        




"""Récuperer les liens des livres de chaque categorie"""
"""Extraire les infos de chaque livres"""
"""Écrire les infos des livres dans un fichier CSV par catégorie"""
"""télécharger et enregistrer l'image de chaque livre"""