from bs4 import BeautifulSoup
from matplotlib.pyplot import text
import requests
from csv import writer

import pandas as pd
from pandas_profiling import ProfileReport

url="https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2510209.m570.l1313&_nkw=lens&_sacat=0"
page=requests.get(url)
soup= BeautifulSoup(page.content, 'html.parser')
lists=soup.find_all('div', class_="s-item__info clearfix")

for list in lists:
    productName=list.h3.text.replace("New Listing","")
    condition=list.find('span', class_="SECONDARY_INFO").text
    try:
        reviewCountString=list.find('span', class_="s-item__reviews-count").text[:6]
        reviewCount=""
        for character in reviewCountString:
            if character.isdigit():
                reviewCount=reviewCount+str(character)
        reviewCount=int(reviewCount)
    except:
        reviewCount=0
    star=list.find('div', class_="x-star-rating")
    try:
        rating=float(star.find('span', class_="clipped").text[:3])
    except:
        rating=0
    price=float(list.find('span', class_="s-item__price").text[1:].replace(",",""))
    try:
        shippingPrice=list.find('span', class_="s-item__shipping").text
    except:
        shippingPrice="Shipping not specified"
    try:
        shippingLocation=list.find('span', class_="s-item__location").text[5:]
    except:
        shippingLocation="Unspecified"
    data=[productName, condition, rating, reviewCount, price, shippingPrice, shippingLocation]
    print(data)