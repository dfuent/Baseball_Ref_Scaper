# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 10:12:57 2020

@author: fuent
"""
from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import Request, urlopen
import re
import pandas as pd
import time
import datetime
import os   
import httplib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

#Option so that selenium doesn't open a new Chrome window
options = webdriver.ChromeOptions()
options.add_argument('--headless')


req = Request("https://factba.se/transcripts/speeches")
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

url = 'https://factba.se/transcripts/speeches'
print(url)




#initiate web driver
driver = webdriver.Chrome(options=options)

#use driver to open url
driver.get(url)


# @Cuong Tran: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python

SCROLL_PAUSE_TIME = 3

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


links = []
for link in soup.findAll('a'):
    links.append(str(link.get('href')))

#print(links)


t = [i for i in links if 'speech' in i]

t = list(set(t))

#print(t)

  
t_1 = time.time()


table = pd.DataFrame()

fin_list = []

for i in t:
    
    loop_time = time.time()
    table_i = pd.DataFrame()
    url = 'https://factba.se/'+ str(i)
    print(url)

    
    #Option so that selenium doesn't open a new Chrome window
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    #initiate web driver
    driver = webdriver.Chrome(options=options)
    
    #use driver to open url
    driver.get(url)
    
    #wait three seconds to load page (probably not necessary)
    time.sleep(4)
    
    #extract page HTML and parse with BeautifulSoup
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    attributes = soup.a.attrs
    
    
  
    try:
    
        
        speaker = soup.findAll(True, {'class':'speaker-label'})
        quote = soup.findAll(True, {'class':'transcript-text-block'})
        
        # j = 0
        # speaker_clean = []
        # quote_clean = []
        # for i in speaker:
        #     speaker_clean.append(str(i.get_attribute("class")))
        #     quote_clean.append(str(quote[j].get_attribute("name")))
        #     j+=1
            
    
        c = 0
        
        for i in speaker:
            
            fin_list.append((i, quote[c], url))
            c += 1
        
    
    except:
        print('Error')

filter(None, fin_list)
 
    ######################################




df = pd.DataFrame.from_records(fin_list,columns = ['Speaker','Transcript', 'Source'])

print(df)

df.to_csv('trump_factbase.txt', index = False)

#%%

