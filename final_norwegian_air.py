#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 15:07:28 2018

@author: default
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 17:12:25 2018

@author: default
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
##########################
######IMPORT SELENIUM#####
##########################
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException 

##import exporting to csv stuff
#import csv

#set working directory
import os
path="/Users/default/Desktop/Python Spyder"
os.chdir(path)

#set working directory
import os
path="/Users/default/Desktop/Python Spyder"
os.chdir(path)
   

##########################
######FUCTIONS ###########
##########################    
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def get_min_by_col(li, col):
    # col - 1 is used to 'hide' the fact lists' indexes are zero-based from the caller
    return min(li, key=lambda x: x[col - 1])[col - 1]

##############################################################
###Get list of possible destinations/departure airports #####
###############################################################

reader = open("destinations.txt", "r")  ##
destinations = reader.read().split('\n')
print("destinations to scrape: ",destinations)

reader = open("origins.txt", "r")  ##
origins = reader.read().split('\n')
print("origins to scrape: ",origins)

##############################
######Launch Website #####
##############################

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")


driver = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver',chrome_options=chrome_options)
all_prices = []
flight_names = []

##############################
######Scrape! ################
##############################

for origin in origins:
        
    for destination in destinations:
        
        driver.get('https://www.norwegian.com/us') #initial website
        #for destination in destinations:
        fly_from = driver.find_element_by_xpath('//*[@id="airport-select-origin"]') #fly from search bar
        time.sleep(1)
        fly_from.clear()
        fly_from.send_keys(origin)
        if origin == "Boston":
            fly_from.send_keys(Keys.DOWN) #looking at all Boston airports rather than 1 Boston airport
        time.sleep(1)
        fly_from.send_keys(Keys.TAB)
        fly_to = driver.find_element_by_xpath('//*[@id="airport-select-destination"]') #fly to locates the search bar
        time.sleep(1)
        fly_to.send_keys(destination)
        time.sleep(1)
        fly_to.send_keys(Keys.TAB)
        time.sleep(2)
        
        driver.find_element_by_xpath('//*[@id="tripType"]/span[2]/label/span[1]').click() #click one way
        driver.find_element_by_xpath('/html/body/main/div[4]/div/div[2]/div[2]/div/div/form/div/div/div/fieldset[5]/div/span[2]/label/span[1]').click() #show low fare calendar
        time.sleep(1)

        
        driver.find_element_by_xpath('//*[@id="searchButton"]').click() #find the arrow and click
        driver.find_element_by_xpath('//*[@id="ctl00_ctl00_MainContentRegion_MainRegion_ctl00_ipcFareCalendarResultOutbound_lnkbNextMonth"]').click() #find the arrow and click
        
        
        airport_name = driver.find_element_by_xpath('//*[@id="aspnetForm"]/table/tbody/tr/td/div[1]/table[1]/tbody/tr/td[1]/div/h1').text #airport name and destination
        flight_names.append(airport_name)
    
        
        month = range(1,32)
        
        price_attributes = []
        time.sleep(2)
        for day in month: #scraping the price for each day of the month
            try:
                price = driver.find_element_by_xpath('//*[@id="OutboundFareCal' + str(day) + '"]/div[3]').text
                price_attributes.append(price) 
            except:
                price_attributes.append('9999')
        price_attributes = [str(element) for element in price_attributes] #make everything a string
        price_attributes = [element.replace(",","") for element in price_attributes] #replace a comma with nothing, preparing to be converted back to int
        price_attributes = [float(element) for element in price_attributes] #make everything a float
        price_attributes #price attributes is now cleaned up
        all_prices.append(price_attributes)
##########################
######Exit ###############
##########################time.sleep(3) # sleep for 3 seconds so you can see the results
driver.quit()

print(all_prices)

#associate that column with the airport flight and destination

minimum_price_list = []
for day in month: #get the minimum price for each day of the month
    print(day)
    min_price = get_min_by_col(all_prices,day)
    minimum_price_list.append(min_price)
    #print(min_price)

print(minimum_price_list)



######getting the flight info associated with each minimum price
flight_info_min_price = [[] for _ in range(31)]
for min_price_list_index, min_price in enumerate(minimum_price_list):
    print(min_price_list_index, min_price)
    for all_prices_index, list_of_prices in enumerate(all_prices):
        print(all_prices_index, list_of_prices)
        #first min price in first list of prices
        if min_price == list_of_prices[min_price_list_index]:
            flight_info_min_price[min_price_list_index].append(flight_names[all_prices_index])
print(flight_info_min_price)
    

###############################################################################
###Output to CSV ##############################################################
###############################################################################
date = []
for i in range(1,32):
    date.append("August " + str(i)) #demo for the month of August
print(date)




import pandas as pd
df = pd.DataFrame({'Date':date})
df['price'] = minimum_price_list
df['flight_info'] = flight_info_min_price

######SORT
df = df.sort_values('price')
df
writer = pd.ExcelWriter('NorwegianAir.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()

print ("done")
