# import re
# price="69 bids"
# totalPr=0
# prices= re.findall(r"[-+]?\d*\.\d+|\d+", price)
# print(int(prices[0]))


from bs4 import BeautifulSoup
import requests
from csv import writer

import re

import pandas as pd
from pandas_profiling import ProfileReport

        
url="https://www.ebay.com/sch/i.html?_from=R40&_nkw=ps5&_sacat=0&LH_TitleDesc=0&rt=nc&LH_All=1"
page=requests.get(url)
soup= BeautifulSoup(page.content, 'html.parser')
lists=soup.find_all('div', class_="s-item__info clearfix")

for list in lists:
    try:
        bidEnd=list.find('span', class_="s-item__time-end")
    except:
        bidEnd="vetena"
    print(bidEnd)



    