
import csv
import math
import os
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from lxml import html

url = 'http://books.toscrape.com/index.html'


def get_page(url):
    #Contenu de la page web
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


def get_books_links(category_link):
#Récupère les liens des livres d'une page, et extrait les données de chaque livre les images
    articles = get_page(category_link).select('h3')
    for tag in articles:
        a = tag.select_one('a')
        link = urljoin (category_link, a['href'])
        csv_file_creation(category_link, link)
        get_image(link, category_link)

def pagination(category_link): 
# Recupère le lien de la page suivante et éxecute la fonction qui récupère les URL des livres d'une page
  get_books_links(category_link)
  if get_page_number(category_link) > 1:
    for page_number in range(2,get_page_number(category_link,1)):      
        next_page_url = urljoin(category_link,'page-'+ str(page_number)+'.html')
        get_books_links(next_page_url)


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

def create_directory(category_link):
  #Créer le répertoire pour chaque catégorie et images 
  category_name = get_category_name(category_link)
  os.mkdir(f'{category_name}/')
  os.mkdir(f'{category_name}/images/')

def csv_file_headlines(category_link):
  #Création de l'entête du fichier CSV
  category_name = get_category_name(category_link)
  headlines = csv_headlines()
  create_directory(category_link)
  with open(f'{category_name}/' + 'Category_' + category_name + '_Books.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, delimiter = ';', fieldnames=headlines)
    writer.writeheader()

def csv_file_creation(category_link, book_link):
  #Création du fichier csv au nom de la catégorie
  category_name = get_category_name(category_link)
  book_data = get_book_data(book_link)
  with open(f'{category_name}/' + 'Category_' + category_name + '_Books.csv', 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(book_data)


def get_image(book_link, category_link):
    #Enregistre l'image de chaque livre dans le dossir dédié
    image = urljoin(book_link, sel(book_link,'.item > img')['src'])  
    image_response = requests.get(image)
    upc = get_book_data(book_link)[1]
    category_name = get_category_name(category_link)
    with open (f'{category_name}/images/' + upc + '.jpg', 'wb') as imagefile:
      imagefile.write(image_response.content)

def main():
  #Boucle sur les URL des catégories stocké dans une liste, y récupère les URL des livres pour en extraire les données et crée le fichier CSV
    start = time.time()
    get_books_category_links()
    for link in books_category_links:
        category_name = get_category_name(link)
        print(f'Extraction des livres de la catégorie {category_name} en cours...')
        csv_file_headlines(link)
        pagination(link)
    print('Extraction Terminé !')
    end = time.time()
    elapsed = end - start
    print(f"Temps d'éxécution : {elapsed}")
       
main()      
