# Homework 3: Python and Web Scraper
# Loren Bushkar, lbb3y
# Resources:
# 1Intro to Web Scraping with Python, Traversy Media, https://www.youtube.com/watch?v=4UcqECQe5Kc
# 2CSV File Reading and Writing, https://docs.python.org/3/library/csv.html
# 3Pandas.read_csv, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html 
# 4Pandas.DataFrame.isin, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.isin.html 
# 5pandas.pivot_table, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.isin.html 
# 6pandas.DataFrame.to_csv, https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html 
# 7Python Histogram Plotting: NumPy, Matplotlib, Pandas & Seaborn, https://realpython.com/python-histograms/ 

import requests # use for scraper 
import csv # use to write scraped data to csv files
import pandas as pd # use for analysis functions and csv read and write
import numpy as np # investigating plotting functionality
import matplotlib.pyplot as plt # investigating plotting functionality
import sys # use to write text file
from bs4 import BeautifulSoup # for scraper
from csv import writer # for csv writer

# set page to be scraped (use requests libary function get)
response = requests.get('https://www.iif.com/Membership/Our-Member-Institutions') 

# use BeautifulSoup to create scraper
soup = BeautifulSoup(response.text, 'html.parser') 

# use id to scrape through member list which is in 5 accordion menus with class membership-accordion-info
members = soup.find(id='dnn_ctr1048_Find_ctl00_lstRecords_pnlItems').find_all(class_='membership-accordion-info')
members4 = soup.find(id='dnn_ctr1052_Find_ctl00_lstRecords_pnlItems').find_all(class_='membership-accordion-info')
members5 = soup.find(id='dnn_ctr1054_Find_ctl00_lstRecords_pnlItems').find_all(class_='membership-accordion-info')
members6 = soup.find(id='dnn_ctr1055_Find_ctl00_lstRecords_pnlItems').find_all(class_='membership-accordion-info')
members7 = soup.find(id='dnn_ctr1056_Find_ctl00_lstRecords_pnlItems').find_all(class_='membership-accordion-info')

# create csv file in which to store scraped data
with open('iifmembers.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = writer(csv_file) # use writer from library csv 
    headers = ['Member', 'Country'] # identify headers for the data
    csv_writer.writerow(headers) # write the headers into the file

# for each id block use a for loop to loop through each listed institution which are separated by div
    for member in members:
        # use BeautifulSoup function select to pull country and member name separate by div
        # use replace functions to clean up dashes and spaces in the page
        country = member.select('div')[0].get_text().replace('- ','').replace('\n','') 
        memberName = member.select('div')[1].get_text().replace('\n','').replace('- ','')
        
        # print(memberName, country) # test output
        # use writer from csv library to write each row within the for loop
        csv_writer.writerow([memberName, country])

# repeat the loop for each id block
    for member4 in members4:
        country = member4.select('div')[0].get_text().replace('- ','').replace('\n','')
        memberName = member4.select('div')[1].get_text().replace('\n','').replace('- ','')
        # print(memberName, country)
        csv_writer.writerow([memberName, country])
    
    for member5 in members5:
        country = member5.select('div')[0].get_text().replace('- ','').replace('\n','')
        memberName = member5.select('div')[1].get_text().replace('\n','').replace('- ','')
        # print(memberName, country)
        csv_writer.writerow([memberName, country])

    for member6 in members6:
        country = member6.select('div')[0].get_text().replace('- ','').replace('\n','')
        memberName = member6.select('div')[1].get_text().replace('\n','').replace('- ','')
        #print(memberName, country)
        csv_writer.writerow([memberName, country])
    
    for member7 in members7:
        country = member7.select('div')[0].get_text().replace('- ','').replace('\n','')
        memberName = member7.select('div')[1].get_text().replace('\n','').replace('- ','')
        # print(memberName, country)
        csv_writer.writerow([memberName, country])

# use pandas library read_csv function to pull the members data into a new dataframe
iifdata = pd.read_csv("/Users/lbushkar/Desktop/Fall 2020 Python Files/iifmembers.csv", encoding='Latin-1')

# print(iifdata)
# print(iifdata.Member)

# set second page to be scraped (use requests library function get)
response2 = requests.get('https://www.baft.org/membership/list-of-members')

# create the scraper using the Beautiful Soup library
soup2 = BeautifulSoup(response2.text, 'html.parser')

# this page is simpler and has a list of firm names in 2 columns so scrap the data using id 
members2 = soup2.find(id='bodyContent_C002_Col00').get_text().split('\n')
members3 = soup2.find(id='bodyContent_C002_Col01').get_text().split('\n')

#print(soup2.prettify()) # use to view page source in a 'prettier' format

# create and open csv file in which to store scraped data
with open('baftmembers.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = writer(csv_file) # use writer from library csv 
    headers = ['Member'] # name header
    csv_writer.writerow(headers) # write header name into file

# for each id block use a for loop to loop through each listed institution which are separated by div
    # members2.to_csv('newtestfile.csv')
    # use for loop to write rows of the firm name into a csv file using the csv library for both id blocks      
    for member2 in members2:
        csv_writer.writerow([member2])  

    for member3 in members3:
        csv_writer.writerow([member3])

# use pandas library read_csv function to pull the members data into a new dataframe
baftdata = pd.read_csv("/Users/lbushkar/Desktop/Fall 2020 Python Files/baftmembers.csv", encoding='Latin-1')

# print(baftdata)

# use pandas isin function to compare dataframes and store in new variable
commonNames = iifdata['Member'].isin(baftdata['Member'])
# for v in commonNames:
#     print(v)

# use sys library to swtich to print output to text file
original = sys.stdout # set current output format as original so we can come back to this
sys.stdout = open('commonMembersReport.txt', 'w') # create and open new text file to generate report
# new dictionary contains all iif member names and whether the isin function returned true or false
newData = {}    
newData = {'Member' : iifdata['Member'], 'Common': commonNames} 
df = pd.DataFrame(newData) # load the new dictionary just created into a pandas dataframe
print(df[df['Common']==True]) # print only the member names from the dataframe where the commonality condition returned true
sys.stdout = original # stop writing to text

# use pandas function pivot table to count the number of members in each country
countryPivot = iifdata.pivot_table(index = ['Country'], values = ['Member'], aggfunc = 'count')
countryPivot.to_csv('iifcountries.csv') # use the very handy pandas to csv file to write the resulting pivot table counts into a csv file

# print(countryPivot)
# countryHist = pd.DataFrame.hist(countryPivot)
# # print(countryHist)
# # xval = ['1','2','3','4','5','6','7','8','9','10']
# # plt.bar(xval,countryHist)
# n, bins, patches = plt.hist(x=countryPivot, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.title('My Very Own Histogram')
# plt.text(23, 45, r'$\mu=15, b=3$')
# maxfreq = n.max()
# # Set a clean upper y-axis limit.
# plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
# plt.show()