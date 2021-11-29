#All Libraries needed to run the code

import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
import urllib.request
import urllib.error
import bs4 #this is beautiful soup
import time
from datetime import datetime
import html
import string
import os.path
from os import path
import csv
import sys
import string
import random
import schedule
from pandas import Series
import pandas as pd
from pandas import DataFrame

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import *
from selenium.common.exceptions import ElementNotInteractableException , TimeoutException


class Google_Scrapper:
    
    def __init__(self): # Intilization Function 
        
        #Containing the keywords
        self.India = [] 
        self.Us = []
        self.UAE = []
        
        #Containing the proxy ports --- set according to luminati proxy manager
        self.PROXY_US = 'http://127.0.0.1:24001'
        self.PROXY_INDIA = 'http://127.0.0.1:24001'
        self.PROXY_UAE = 'http://127.0.0.1:24001'
    
    
    def RefreshIP(self): #Refreshing IP's provided by luminati so that we get new Ip's to work with everyday
        
        #opening the file
        file = open("RefreshIP.txt")  
    
        # Running file on terminal 
        os.system(file.read())

        # closing the file 
        file.close() 
        
        
    def Keyword_extraction(self, Country): #Extracts keywords from google sheet named --- Your Excel Sheet
        
        try:
            
            # Connecting to Drive and Sheets API
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
            client = gspread.authorize(creds)
            sheet = client.open('') #The name of your sheet from google sheets 
            
            WORKSHEET  = sheet.worksheet(Country)
            
            Worksheet_keywords = WORKSHEET.col_values(1)
            Worksheet_keywords.remove("KEYWORDS")
            
            # returning all the Keywords from the worksheet
            return Worksheet_keywords
        
        # If could not connect to google server remotely access the keyword list stored in the system
        except:
            list_of_stores = []
            with open(Country + '.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    #print(row[0])
                    if row is not None:
                        list_of_stores.append(row[0])
            csv_file.close()
            return list_of_stores
                        
    
        
    # Excel Updation in google sheets directly ---- 30 days data will reamin in the sheet    
    def Excel_Updation(self, India_Dict, Us_Dict, UAE_Dict):
        
        #Connecting to Drive and Sheets API
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open('') #The name of your sheet from google sheets 
        
        # Accessing all 3 Sheets 
        India = sheet.worksheet('India')
        US = sheet.worksheet('US')
        UAE = sheet.worksheet('UAE')
        
        # Get all records for complete updation of the google sheet
        list_India_worksheet = India.get_all_records()
        list_US_worksheet = US.get_all_records()
        list_UAE_worksheet = UAE.get_all_records()
        
        # Dataframe created for all records
        India_df = pd.DataFrame.from_dict(list_India_worksheet)
        US_df = pd.DataFrame.from_dict(list_US_worksheet)
        UAE_df = pd.DataFrame.from_dict(list_UAE_worksheet)
        
        
        list_temp_India = []
        list_temp_US = []
        list_temp_UAE = []

        # Empty space --- so that list index out of bounds error does not appear
        for i_temp in range(len(India_df['KEYWORDS'])):
            list_temp_India.append('')
        for i_temp in range(len(US_df['KEYWORDS'])):
            list_temp_US.append('')
        for i_temp in range(len(UAE_df['KEYWORDS'])):
            list_temp_UAE.append('')
        
        
        # today's Date 
        today_datetime = datetime.now()
        date_today= str(today_datetime.strftime('%d')) + '-' + today_datetime.strftime('%m') +'-'+ today_datetime.strftime('%Y')
        
        # Updation of blank data onto the dataframes
        India_df[date_today] = list_temp_India
        US_df[date_today] = list_temp_US
        UAE_df[date_today] = list_temp_UAE

        
        # Updation of data according to the dictionary values recieved during scrapping 
        for i_temp,j_temp in zip(India_Dict.values(),India_Dict.keys()):

            try:
                India_df[date_today].loc[India_df['KEYWORDS'] == j_temp] = i_temp

            except:
                pass
        
        for i_temp,j_temp in zip(Us_Dict.values(),Us_Dict.keys()):

            try:
                US_df[date_today].loc[US_df['KEYWORDS'] == j_temp] = i_temp

            except:
                pass
        
        for i_temp,j_temp in zip(UAE_Dict.values(),UAE_Dict.keys()):

            try:
                UAE_df[date_today].loc[UAE_df['KEYWORDS'] == j_temp] = i_temp

            except:
                pass
        
        
        # Check for seeing if we have crossed the 30 day limit for columns --- If yes will drop the first column 
        try: # If this fails that means there was no records of ranks to begin with
            date_dt1 = datetime.strptime(India_df.columns[1], '%d-%m-%Y')
            date_dt2 = datetime.strptime(India_df.columns[-1], '%d-%m-%Y')
            if(str(date_dt2 - date_dt1)[0:2] == '31'):
            #print('true') 
                India_df.drop([India_df.columns[1]], axis='columns', inplace=True)
        
        except:
            pass
        
        try:
            date_dt1 = datetime.strptime(US_df.columns[1], '%d-%m-%Y')
            date_dt2 = datetime.strptime(US_df.columns[-1], '%d-%m-%Y')
            if(str(date_dt2 - date_dt1)[0:2] == '31'):
            #print('true') 
                US_df.drop([US_df.columns[1]], axis='columns', inplace=True)
        except:
            pass
        
        try:    
            date_dt1 = datetime.strptime(UAE_df.columns[1], '%d-%m-%Y')
            date_dt2 = datetime.strptime(UAE_df.columns[-1], '%d-%m-%Y')
            if(str(date_dt2 - date_dt1)[0:2] == '31'):
            #print('true') 
                UAE_df.drop([UAE_df.columns[1]], axis='columns', inplace=True)
        except:
            pass
        
        
        
        # Will update the google sheets according to the data present in dataframes
        India.update([India_df.columns.values.tolist()] + India_df.values.tolist())
        US.update([US_df.columns.values.tolist()] + US_df.values.tolist())
        UAE.update([UAE_df.columns.values.tolist()] + UAE_df.values.tolist())
        
        
        
        
        
        
        
    def India_site(self): #Indian site scrapper 
        
        
        # Calling Keyword_Extraction to get the keywords for scrapping the ranks of the keywords
        self.India = self.Keyword_extraction('India')
        #self.India = self.India[0:2]
        
        
        # Setting up the proxy for Luminati 
        proxy_india = Proxy()
        proxy_india.http_proxy = self.PROXY_INDIA
        proxy_india.https_proxy = self.PROXY_INDIA
        proxy_india.ftp_proxy = self.PROXY_INDIA
        proxy_india.sslProxy = self.PROXY_INDIA
        proxy_india.no_proxy = "localhost" #etc... ;)
        proxy_india.proxy_type = ProxyType.MANUAL
        
        
        iterator_bot = 1 # iterator_bot for creating scheduled stops so that we don't overuse the proxies
        dict_of_rank = {} # Empty ranker dcitionary 

        PATH = "/chromedriver" # path of chromedriver

        # incognito settings for chrome
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        
        # adding proxy, incognito and path to chromedriver
        capabilities = webdriver.DesiredCapabilities.CHROME
        proxy_india.add_to_capabilities(capabilities)
        driver = webdriver.Chrome( desired_capabilities=capabilities,executable_path= PATH )

        driver.get('https://www.google.com')
        bot_avoider_counter = 0

        while(True): #Loop will end when all the keywords ranks have been found    


            if (iterator_bot >= 50): # if iterator_bot is greater than 50 the excetion will break for 30 seconds
                    
                    driver.quit()
                    time.sleep(30)
                    driver = webdriver.Chrome( desired_capabilities=capabilities,executable_path= PATH )
                    driver.get("https://www.google.com")
                    iterator_bot = 1
            
            count_rank = 1 # Variable which will finally provide us with rank of each keywords 

            # Main loop will break if keyword_list string is completed
            if bot_avoider_counter == len(self.India):
                break

            while(True):# loop to find a single keywords rank

                # Will break if last dictionary keys is equal to the current keyword for which we are finding the rank
                if  (len(dict_of_rank.keys()) != 0) and (self.India[bot_avoider_counter] in list(dict_of_rank.keys())[-1]):
                    break
                
                # Maximum count after which the loop itself will automatically exit 
                if count_rank > 100:
                    dict_of_rank[self.India[bot_avoider_counter]] = 'N/A'
                    break
                
                #Keyword being run for the first time in the loop
                if (count_rank == 1):
                    
                    try: # Waiting for the driver to find the search element q --- q - name-address in html for search-tb of google
                        search1 = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, "q"))
                        )


                        search1.clear()
                        search1.send_keys(self.India[bot_avoider_counter])
                        search1.send_keys(Keys.RETURN)
                        iterator_bot = iterator_bot + 1


                    except: # if we cannot find --- Either bot or internet slow to respond
                        
                        driver.quit()
                        time.sleep(118)
                        driver = webdriver.Chrome( desired_capabilities=capabilities,executable_path=PATH )
                        driver.get('https://www.google.com/')
                        bot_avoider_counter = bot_avoider_counter - 1
                        break

                
                else: #If we are not able to find the keyword on the first page, this code will run on every page till we cannot find pages or count > 100
                    
                    try: #Wait for the driver to locate the NEXT element id for clickable UI interaction
                        search = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//a[@id='pnnext']"))
                        )

                        
                        search.click()
                        iterator_bot = iterator_bot + 1
                    

                    except ElementNotInteractableException: # When search.click() fails --- usually when accaepting cookies in google

                        
                        driver.quit()
                        driver = webdriver.Chrome( desired_capabilities=capabilities,executable_path=PATH )
                        driver.get('https://www.google.com/')
                        bot_avoider_counter = bot_avoider_counter - 1
                        break

                    except:# When bot or time-out exception takes place
                        
                        try: # to find out if the exception was due to the bot or we could not find NEXT--element for UI-interaction
                            
                            
                            search = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.NAME, "q"))
                            )
                            
                            #If the code enters this segement it means we are on the last page for the keyword
                            if (len(dict_of_rank.keys()) != 0) and (self.India[bot_avoider_counter] in list(dict_of_rank.keys())[-1]):
                                break
                            else:
                                dict_of_rank[self.India[bot_avoider_counter]] = 'N/A'                     
                            iterator_bot = iterator_bot + 1
                            break
                            
                        except:# Bot detected
                            driver.quit()
                            time.sleep(118)
                            driver = webdriver.Chrome(desired_capabilities=capabilities,executable_path=PATH )
                            driver.get('https://www.google.com/')
                            bot_avoider_counter = bot_avoider_counter - 1
                            break



                try: # Code to scrape the google page 

                    WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, "q"))
                        )


                    source = bs4.BeautifulSoup(driver.page_source)# Scrapping using beautifulsoup

                    for i_temp in source.find_all('div',{'id':'search'}):# ID-Address - SEARCH 

                        length_of_all_result = len(i_temp.contents[0].contents[2])

                        
                        # if currnt keyword already present in dictionary break the loop and move to next keyword
                        if (len(dict_of_rank.keys()) != 0) and (self.India[bot_avoider_counter] in list(dict_of_rank.keys())[-1]):
                            break

                        # if count exceeds the maximum count exit the loop
                        if count_rank > 100:
                            break



                        # HTML parser loop
                        for j_temp in range(length_of_all_result):
                            temp_check_class = i_temp.contents[0].contents[2].contents[j_temp].get('class')

                            
                            # Loop to find normal results --- WEB RESULTS
                            if ((temp_check_class is not None) and ("".join(temp_check_class) == 'g')):

                                link_tag_of_g = i_temp.contents[0].contents[2].contents[j_temp].find('a')
                                str_link = str(link_tag_of_g.get('href'))

                                if  str_link.find('') == -1: # Name for your Website
                                    count_rank = count_rank + 1
                                    if count_rank > 100:
                                        break
                                else:
                                    dict_of_rank[self.India[bot_avoider_counter]] = count_rank

                                    break

                                    
                            # Loop to find snippet results --- SNIPPET
                            elif (temp_check_class is not None) and ("".join(temp_check_class) == 'gmnr-cg-blk'):

                                snippet_link = i_temp.contents[0].contents[2].contents[j_temp].contents[0].contents[0].contents[0].contents[1]
                                snippet_link_length = len(i_temp.contents[0].contents[2].contents[j_temp].contents[0].contents[0].contents[0].contents[1])

                                for snippet_link_length_count in range(snippet_link_length):

                                    snippet_link.contents[snippet_link_length_count].get('class')
                                    if (("".join(snippet_link.contents[snippet_link_length_count].get('class')) is not None ) and ("".join(snippet_link.contents[snippet_link_length_count].get('class')  )) == 'g'):
                                        link_tag_of_snippet=snippet_link.contents[snippet_link_length_count].find('a')
                                        str_snippet_link = link_tag_of_snippet.get('href')


                                if  str_snippet_link.find('') == -1: # Name for your Website
                                    count_rank = count_rank + 1

                                    if count_rank > 100:
                                        break
                                else:
                                    dict_of_rank[self.India[bot_avoider_counter]] = 'snippet'
                                    break

                except: # if it fails bot was detected
                    driver.quit()
                    time.sleep(118)
                    driver = webdriver.Chrome(desired_capabilities=capabilities,executable_path=PATH )
                    driver.get('https://www.google.com/')
                    bot_avoider_counter = bot_avoider_counter - 1
                    break

            bot_avoider_counter = bot_avoider_counter + 1 # bot_counter ensures we traverse all the strings
            
        
        driver.quit() #Finally quit google
        return dict_of_rank# Return the dictionary values
    
    
    def US_site(self): # US scrapping site --- NOTE -- Same comments as India_Site()
        
        self.Us = self.Keyword_extraction('US')
        #self.Us = self.Us[0:2]
        
        proxy_us = Proxy()
        proxy_us.http_proxy = self.PROXY_US
        proxy_us.https_proxy = self.PROXY_US
        proxy_us.ftp_proxy = self.PROXY_US
        proxy_us.sslProxy = self.PROXY_US
        proxy_us.no_proxy = "localhost" #etc... ;)
        proxy_us.proxy_type = ProxyType.MANUAL
        
        iterator_bot = 1
        dict_of_rank = {}  # outside the main loop

        PATH = "/chromedriver"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")

        capabilities = webdriver.DesiredCapabilities.CHROME
        proxy_us.add_to_capabilities(capabilities)
        driver = webdriver.Chrome( desired_capabilities=capabilities,executable_path= PATH)

        driver.get('https://www.google.com')
        bot_avoider_counter = 0

        while(True):    


            if (iterator_bot >= 50):
                    
                    driver.quit()
                    time.sleep(30)
                    driver = webdriver.Chrome( desired_capabilities=capabilities,executable_path= PATH )
                    driver.get("https://www.google.com")
                    iterator_bot = 1
                    
            count_rank = 1 # inside the main loop

            if bot_avoider_counter == len(self.Us):
                break

            while(True):


                if  (len(dict_of_rank.keys()) != 0) and (self.Us[bot_avoider_counter] in list(dict_of_rank.keys())[-1]):
                    break

                    
                if count_rank > 100:
                    dict_of_rank[self.Us[bot_avoider_counter]] = 'N/A'
                    break

                    
                if (count_rank == 1):
                    try:
                        search1 = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, "q"))
                        )


                        search1.clear()
                        search1.send_keys(self.Us[bot_avoider_counter])
                        search1.send_keys(Keys.RETURN)
                        iterator_bot = iterator_bot + 1


                    except:
                        
                        driver.quit()
                        time.sleep(118)
                        driver = webdriver.Chrome( desired_capabilities=capabilities,executable_path=PATH )
                        driver.get('https://www.google.com/')
                        bot_avoider_counter = bot_avoider_counter - 1
                        break

                else:
                    try:
                        search = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//a[@id='pnnext']"))
                        )

                        search.click()
                        iterator_bot = iterator_bot + 1
                        

                    except ElementNotInteractableException:

                        
                        driver.quit()
                        driver = webdriver.Chrome( desired_capabilities=capabilities,executable_path=PATH )
                        driver.get('https://www.google.com/')
                        bot_avoider_counter = bot_avoider_counter - 1
                        break

                    except:
                        try:
                            search = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.NAME, "q"))
                            )


                            if (len(dict_of_rank.keys()) != 0) and (self.Us[bot_avoider_counter] in list(dict_of_rank.keys())[-1]):
                                break
                            else:
                                dict_of_rank[self.Us[bot_avoider_counter]] = 'N/A'
                            iterator_bot = iterator_bot + 1
                            break
                            
                        except:
                            
                            driver.quit()
                            time.sleep(118)
                            driver = webdriver.Chrome(desired_capabilities=capabilities,executable_path=PATH )
                            driver.get('https://www.google.com/')
                            bot_avoider_counter = bot_avoider_counter - 1
                            
                            break



                try:

                    WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, "q"))
                        )


                    source = bs4.BeautifulSoup(driver.page_source)

                    for i_temp in source.find_all('div',{'id':'search'}):

                        length_of_all_result = len(i_temp.contents[0].contents[2])

                        
                        if (len(dict_of_rank.keys()) != 0) and (self.Us[bot_avoider_counter] in list(dict_of_rank.keys())[-1]):
                            break

                            
                        if count_rank > 100:
                            break



                        for j_temp in range(length_of_all_result):
                            temp_check_class = i_temp.contents[0].contents[2].contents[j_temp].get('class')

                            if ((temp_check_class is not None) and ("".join(temp_check_class) == 'g')):

                                link_tag_of_g = i_temp.contents[0].contents[2].contents[j_temp].find('a')
                                str_link = str(link_tag_of_g.get('href'))

                                if  str_link.find('') == -1: # Name for your Website
                                    count_rank = count_rank + 1
                                    if count_rank > 100:
                                        break
                                else:
                                    dict_of_rank[self.Us[bot_avoider_counter]] = count_rank

                                    break

                            elif (temp_check_class is not None) and ("".join(temp_check_class) == 'gmnr-cg-blk'):

                                snippet_link = i_temp.contents[0].contents[2].contents[j_temp].contents[0].contents[0].contents[0].contents[1]
                                snippet_link_length = len(i_temp.contents[0].contents[2].contents[j_temp].contents[0].contents[0].contents[0].contents[1])

                                for snippet_link_length_count in range(snippet_link_length):

                                    snippet_link.contents[snippet_link_length_count].get('class')
                                    if (("".join(snippet_link.contents[snippet_link_length_count].get('class')) is not None ) and ("".join(snippet_link.contents[snippet_link_length_count].get('class')  )) == 'g'):
                                        link_tag_of_snippet=snippet_link.contents[snippet_link_length_count].find('a')
                                        str_snippet_link = link_tag_of_snippet.get('href')


                                if  str_snippet_link.find('') == -1: # Name for your Website
                                    count_rank = count_rank + 1

                                    if count_rank > 100:
                                        break
                                else:
                                    dict_of_rank[self.Us[bot_avoider_counter]] = 'snippet'
                                    break

                except:
                    
                    driver.quit()
                    time.sleep(118)
                    driver = webdriver.Chrome(desired_capabilities=capabilities,executable_path=PATH )
                    driver.get('https://www.google.com/')
                    bot_avoider_counter = bot_avoider_counter - 1
                    break

            bot_avoider_counter = bot_avoider_counter + 1
            
        driver.quit()
        return dict_of_rank
    
    
    def Uae_site(self):# UAE site scrapper ---- NOTE ---- Comments same as India_site
        
        self.UAE = self.Keyword_extraction('UAE')
        #self.UAE = self.UAE[0:2]
        
        proxy_uae = Proxy()
        proxy_uae.http_proxy = self.PROXY_UAE
        proxy_uae.https_proxy = self.PROXY_UAE
        proxy_uae.ftp_proxy = self.PROXY_UAE
        proxy_uae.sslProxy = self.PROXY_UAE
        proxy_uae.no_proxy = "localhost" #etc... ;)
        proxy_uae.proxy_type = ProxyType.MANUAL
        
        iterator_bot = 1
        dict_of_rank = {}  # outside the main loop

        PATH = "/chromedriver"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")

        capabilities = webdriver.DesiredCapabilities.CHROME
        proxy_uae.add_to_capabilities(capabilities)
        driver = webdriver.Chrome( desired_capabilities=capabilities,executable_path= PATH )

        driver.get('https://www.google.com')
        bot_avoider_counter = 0

        while(True):    


            if (iterator_bot >= 50):
                    driver.quit()
                    time.sleep(30)
                    driver = webdriver.Chrome( desired_capabilities=capabilities,executable_path= PATH )
                    driver.get("https://www.google.com")
                    iterator_bot = 1
                    
            count_rank = 1 # inside the main loop

            
            
            if bot_avoider_counter == len(self.UAE):
                break

                
                
            while(True):


                if  (len(dict_of_rank.keys()) != 0) and (self.UAE[bot_avoider_counter] in list(dict_of_rank.keys())[-1]):
                    break

                if count_rank > 100:
                    dict_of_rank[self.UAE[bot_avoider_counter]] = 'N/A'
                    break

                    
                if (count_rank == 1):
                    try:
                        search1 = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, "q"))
                        )


                        search1.clear()
                        search1.send_keys(self.UAE[bot_avoider_counter])
                        search1.send_keys(Keys.RETURN)
                        iterator_bot = iterator_bot + 1


                    except:
                        driver.quit()
                        time.sleep(118)
                        driver = webdriver.Chrome( desired_capabilities=capabilities,executable_path=PATH )
                        driver.get('https://www.google.com/')
                        bot_avoider_counter = bot_avoider_counter - 1
                        break

                else:
                    try:
                        search = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//a[@id='pnnext']"))
                        )

                        search.click()
                        iterator_bot = iterator_bot + 1
                        

                    except ElementNotInteractableException:

                        
                        driver.quit()
                        driver = webdriver.Chrome( desired_capabilities=capabilities,executable_path=PATH )
                        driver.get('https://www.google.com/')
                        bot_avoider_counter = bot_avoider_counter - 1
                        break

                    except:
                        try:
                            search = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.NAME, "q"))
                            )

                            if (len(dict_of_rank.keys()) != 0) and (self.UAE[bot_avoider_counter] in list(dict_of_rank.keys())[-1]):
                                break
                            else:
                                dict_of_rank[self.UAE[bot_avoider_counter]] = 'N/A'
                            iterator_bot = iterator_bot + 1
                            break
                            
                            
                        except:
                            driver.quit()
                            time.sleep(118)
                            driver = webdriver.Chrome(desired_capabilities=capabilities,executable_path=PATH )
                            driver.get('https://www.google.com/')
                            bot_avoider_counter = bot_avoider_counter - 1
                            break



                try:

                    WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, "q"))
                        )


                    source = bs4.BeautifulSoup(driver.page_source)

                    for i_temp in source.find_all('div',{'id':'search'}):

                        length_of_all_result = len(i_temp.contents[0].contents[2])

                        if (len(dict_of_rank.keys()) != 0) and (self.UAE[bot_avoider_counter] in list(dict_of_rank.keys())[-1]):
                            break

                        if count_rank > 100:
                            break



                        for j_temp in range(length_of_all_result):
                            temp_check_class = i_temp.contents[0].contents[2].contents[j_temp].get('class')

                            if ((temp_check_class is not None) and ("".join(temp_check_class) == 'g')):

                                link_tag_of_g = i_temp.contents[0].contents[2].contents[j_temp].find('a')
                                str_link = str(link_tag_of_g.get('href'))

                                if  str_link.find('') == -1: # Name for your Website
                                    count_rank = count_rank + 1
                                    if count_rank > 100:
                                        break
                                else:
                                    dict_of_rank[self.UAE[bot_avoider_counter]] = count_rank

                                    break

                            elif (temp_check_class is not None) and ("".join(temp_check_class) == 'gmnr-cg-blk'):

                                snippet_link = i_temp.contents[0].contents[2].contents[j_temp].contents[0].contents[0].contents[0].contents[1]
                                snippet_link_length = len(i_temp.contents[0].contents[2].contents[j_temp].contents[0].contents[0].contents[0].contents[1])

                                for snippet_link_length_count in range(snippet_link_length):

                                    snippet_link.contents[snippet_link_length_count].get('class')
                                    if (("".join(snippet_link.contents[snippet_link_length_count].get('class')) is not None ) and ("".join(snippet_link.contents[snippet_link_length_count].get('class')  )) == 'g'):
                                        link_tag_of_snippet=snippet_link.contents[snippet_link_length_count].find('a')
                                        str_snippet_link = link_tag_of_snippet.get('href')


                                if  str_snippet_link.find('') == -1: # Name for your Website
                                    count_rank = count_rank + 1

                                    if count_rank > 100:
                                        break
                                else:
                                    dict_of_rank[self.UAE[bot_avoider_counter]] = count_rank
                                    break

                except:
                    driver.quit()
                    time.sleep(118)
                    driver = webdriver.Chrome(desired_capabilities=capabilities,executable_path=PATH )
                    driver.get('https://www.google.com/')
                    bot_avoider_counter = bot_avoider_counter - 1
                    break

            bot_avoider_counter = bot_avoider_counter + 1
        driver.quit()
        return dict_of_rank
    
def main_run(): # Calling th main function to execute the class
    Class_scrape = Google_Scrapper()
    
    India_Dict = Class_scrape.India_site()
    US_Dict = Class_scrape.US_site()
    UAE_Dict = Class_scrape.Uae_site()
    Class_scrape.Excel_Updation(India_Dict,US_Dict,UAE_Dict)
    Class_scrape.RefreshIP()
    
    
schedule.every().day.at("05:30").do(main_run)
while True:
    schedule.run_pending()    

