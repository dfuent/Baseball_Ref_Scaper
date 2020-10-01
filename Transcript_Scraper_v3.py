# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 10:12:57 2020

@author: fuent
"""
from bs4 import BeautifulSoup, SoupStrainer
from urllib.request import Request, urlopen
import pandas as pd
import time
import datetime
import os   
import sys
import io
from selenium import webdriver

def transcript_scraper():
    #Option so that selenium doesn't open a new Chrome window
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    t_0 = time.time()
    hd = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    
    root = 'https://www.debates.org/voter-education/debate-transcripts'
    
    req = Request(root, headers = hd)
    html_page = urlopen(req).read()
    
    
    soup = BeautifulSoup(html_page, "lxml")
    
    
    #initiate web driver
    driver = webdriver.Chrome(options=options)
    
    #use driver to open url
    driver.get(root)
    
    
    links = []
    for link in soup.findAll('a'):
        links.append(str(link.get('href')))
    
    
    t = [i for i in links if 'transcript' in i]
    
    t = list(set(t))
      
    
    fin_dict = {}
    
    for i in t:
        
        loop_time = time.time()

        url = 'https://www.debates.org/' + str(i)
        #print(url)
    
        
        #Option so that selenium doesn't open a new Chrome window
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        
        #initiate web driver
        driver = webdriver.Chrome(options=options)
        
        #use driver to open url
        driver.get(url)
        
        #wait three seconds to load page (probably not necessary)
        time.sleep(3)
        
        #extract page HTML and parse with BeautifulSoup
        html=driver.page_source
        soup=BeautifulSoup(html,'html.parser')
        
        f = io.open('debate_final.txt', 'a', encoding = 'utf-8') # open file for appending ('a')
        
        h = soup('h1')
        h = str(h)[1:-1].replace('<h1>', '').replace('</h1>', '')
        #print(h)
          
        tr = str(soup('p'))
        spl_tr = tr.split('</p>')
        
        l = 1
        speaker = ''
        for j in spl_tr:
            j = j.replace('<p>', '')
            j = j.replace('</p>', '')
            j = j[2:].strip()
            first_word = j.split(' ', 1)[0].strip()
            
            try: 
                last_char = first_word[-1]
                
            except:
                last_char = 0

            #print(last_char)
            try:
            
                if last_char == ':' and first_word.upper() == first_word:
                    #print(True)
                    speaker = first_word.replace(':', '')
                    print(speaker)
            except:
                
                continue
                    
            fin_dict[h + '|' + str(l)] = (speaker, j) 
            f.write(str(l) +',' + h + ',' + speaker + ',' +  j)
            
            l += 1
    
        print('Loop {0} for {1} took {2: .2f} seconds.'.format(l, h, time.time()-loop_time))

     
        ######################################
    print('Finished in {0: .2f} seconds'.format(time.time()-t_0))
    return fin_dict



#%%

t_dict = transcript_scraper()

#%%


j = ' LEHRER: All right, moving'

j = j.strip()
j = j.split(' ', 1)[0][-1] == ':' and j.split(' ', 1)[0][0:len(j)-1].upper() == j.split(' ', 1)[0][0:len(j)-1]

#print(j)

#test.split(' ', 1)[0:len(test.split(' ', 1))-1]


