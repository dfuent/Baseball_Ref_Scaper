def yearly_baseball_stats(fin_year = 2020, n_years = 10):
    
    #dependencies
    import pandas as pd
    import time
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import datetime
    import os

    
    t_1 = time.time()

    #navigate to baseball-reference.com to extract batter stats
    
    table = pd.DataFrame()
    for i in range(n_years):
        
        loop_time = time.time()
        table_i = pd.DataFrame()
        print('Year = {0}'.format(fin_year - i))
        url = 'https://www.baseball-reference.com/leagues/MLB/'+str(fin_year - i)+'-standard-batting.shtml'
    
        
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
        
        #find the table with batter statistics by its ID
        tableHTML=soup.find(id="players_standard_batting")
        
        #use pandas to read the table into a DataFrame
        table_i=table_i.append(pd.DataFrame(pd.read_html(str(tableHTML))[0]))      
        
        #add the date to the table - maybe for time series analysis later
        #table_i['Date'] = datetime.datetime.today().date()
        
        table_i['Year'] = fin_year - i   
        
        table = table.append(table_i)
        print('Cumulative size of data table: {0} rows'.format(table['Name'].count()))
        print('Year {0} loop took {1: .4f} seconds'.format(fin_year - i, time.time()-loop_time))
    
    #Right now there are headers every 25 rows, remove the intermittent headers
    table = table[table['Rk'] != 'Rk']
    
    #Right now there's a summary row at the bottom, remove it
    table = table[table['Name'] != 'LgAvg per 600 PA']
    
    #set the index
    table = table.reset_index().drop(columns='index')    
    
    print('Time check before export: {0: .4f}'.format(time.time()-t_1))

    
    table.to_csv('br_table_' + str(fin_year - (n_years-1)) +'_to_'+str(fin_year) + '.csv', index = False)
    
    print('Table saved in br_table.csv. Total time: {0: .4f}s'.format(time.time()-t_1))
    #return table
        


yearly_baseball_stats(1999, 5)




