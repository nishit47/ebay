from bs4 import BeautifulSoup
import requests
from csv import writer

import re

import pandas as pd
from pandas_profiling import ProfileReport

productInput=input("What product are you looking for? \n >>")

product=""
for character in productInput:
    if character.isspace():
        product=product+"+"
    else:
        product=product+character
        
url="https://www.ebay.com/sch/i.html?_from=R40&_nkw="+product+"&_sacat=0&LH_TitleDesc=0&rt=nc&LH_All=1&_ipg=240&_"
page=requests.get(url)
soup= BeautifulSoup(page.content, 'html.parser')
lists=soup.find_all('div', class_="s-item__info clearfix")

dataName=input("Save Database As: \n >>")
dataNameOutput=dataName+".csv"

outputName=input("Save Report As: \n >>")
outputNameHtml=outputName+".html"

with open(dataNameOutput, 'w', encoding='utf8', newline='') as f:
    thewriter=writer(f)
    heading=["Name", "Condition", "Rating", "Number Of Reviews", "Price", "Shipping Cost", "Shipped from", "Is for auction?", "Number Of Bids", "Time left for bidding"]
    thewriter.writerow(heading)

    for pageNumber in range(2,6): #pageNumber=1+actualPageNumber because url changes after the inner loop
        page=requests.get(url)
        soup= BeautifulSoup(page.content, 'html.parser')
        lists=soup.find_all('div', class_="s-item__info clearfix")
        print(url)

        for list in lists:
            productName=list.h3.text.replace("New Listing","")
            try:
                condition=list.find('span', class_="SECONDARY_INFO").text
            except:
                condition="unavailable"
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
                rating="unrated"
            try:
                price=float(list.find('span', class_="s-item__price").text.replace(",","").replace("$",""))
            except: 
                #for price ranges, it takes average of the two prices 
                price=list.find('span', class_="s-item__price").text.replace(",","").replace("$","")
                totalPr=0
                prices= re.findall(r"[-+]?\d*\.\d+|\d+", price)
                for pr in prices:
                    totalPr+=float(pr)
                AvPr=totalPr/2
                price=AvPr
            try:
                shippingPrice=list.find('span', class_="s-item__shipping").text
            except:
                shippingPrice="Shipping not specified"
            try:
                shippingLocation=list.find('span', class_="s-item__location").text[5:]
            except:
                shippingLocation="Unspecified"
            try:
                bidCountString=list.find('span', class_="s-item__bids s-item__bidCount").text
                bidCount=""
                for character in bidCountString:
                    if character.isdigit():
                        bidCount=bidCount+character
                bidCount=int(bidCount)
                bid="yes"
            except:
                bidCount=0
                bid="No"
            try:
                bidTimeLeft=list.find('span', class_="s-item__time-left").text
            except:
                bidTimeLeft="N/A"
            data=[productName, condition, rating, reviewCount, price, shippingPrice, shippingLocation, bid, bidCount, bidTimeLeft]
            print(data)
            thewriter.writerow(data)

        #going to the next page number
        if pageNumber==2:
            url=url+"pgn="+str(pageNumber)
        else:
            url=url[:-1]+str(pageNumber)

df=pd.read_csv(dataNameOutput)
duplicatesRemoved=df.drop_duplicates()
duplicatesRemoved.to_csv(dataNameOutput)

df=pd.read_csv(dataNameOutput)
profile=ProfileReport(df)
profile.to_file(output_file=outputNameHtml)