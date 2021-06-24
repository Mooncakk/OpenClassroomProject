
import requests
from bs4 import BeautifulSoup
from lxml import html
import csv

response = requests.get("http://books.toscrape.com/catalogue/join_902/index.html")
url = response.url
soup = BeautifulSoup(response.content, "lxml")


def sel(tag, num=0):
    info = soup.select(tag)
    return info[num]

img_url = sel("img")

with open("data_book.csv", "w") as csvfile:
    csvfile.write("Product_page_url : " + url + "\n" + 
    "Universal_product_code : " + sel("td").text +"\n" +
    "Title : " + sel("h1").text + "\n" +
    "Price_including_tax : " + sel("td", 2).text + "\n" +
    "Price_excliding_tax : " + sel("td", 3).text + "\n" +
    "Number_available : " + sel("td", 5).text + "\n" +
    "Product_description : " + sel("p", 3).text + "\n" +
    "Category : " + sel("a", 3).text + "\n" +
    "Review_rating : " + sel("td", 6).text + "\n" +
    "Image_url : " + str(img_url))

