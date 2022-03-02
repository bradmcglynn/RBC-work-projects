#Recipient History Checker Script
import pandas as pd
import numpy as np
recipient_path = "abc.csv"
recipient_df = pd.read_csv(recipient_path, encoding="latin-1", low_memory=False)
recipient_df["FULL NAME"] = recipient_df["RECIPIENT FIRST NAME"] + " " + recipient_df["RECIPIENT LAST NAME"]

notice_connect_path = "xyz.csv"
notice_connect_df = pd.read_csv(notice_connect_path, encoding="latin-1", low_memory=False)

print(notice_connect_df)
matched_name_list = []
name_counter = 2
recipient_counter = 2

recipient_name_list = np.array(recipient_df["FULL NAME"])
notice_connect_name_list = np.array(notice_connect_df["Name"])

for name in notice_connect_name_list:
    for full_name in recipient_name_list:

        if name == full_name:
            matched_name_list.append([name, name_counter, recipient_counter])
        recipient_counter += 1
    name_counter += 1
    recipient_counter = 2

print(matched_name_list)
export_file = pd.DataFrame(matched_name_list)

export_file.drop_duplicates(inplace=True)

export_file.to_csv("exported_names v2.csv")


# NoticeConnect Scraper Script
# have to use conda interpreter w/ python 3.7
# Alt + Shift + E to run just highlighted lines
# Shift + scroll to view horizontally
# to delete variables: del(variable_name)
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import os
import time
# for regular expressions (RegEx), a sequence of characters that forms a search pattern
# can be used to check if a string contains the specified search pattern
import re
import shutil
from shutil import copyfile
from datetime import datetime


# where chromedriver app is located
num_pages = int(input("Enter number of pages you would like to scrape: "))
num_pages += 1
month = input("Enter current month: ")
year = input("Enter current year: ")

driver = webdriver.Chrome(r"chromedriver.exe")
csv_data = pd.DataFrame()


for i in range(1, num_pages):
    listsURL = "https://www.noticeconnect.com/notices/estate/?page={}".format(i)
    # get() method will navigate to a page given by URL
    driver.get(listsURL)
    # allows page to load in properly
    driver.set_page_load_timeout(10)

    name_list = []
    city_list = []
    time.sleep(2)
    for j in range(1, 16):
        xpath = '/html/body/div[2]/div[4]/div/div/div/div/div[2]/table/tbody/tr[{}]/td[1]/a'.format(j)

        name = driver.find_element_by_xpath(xpath).text

        xpath2 = '/html/body/div[2]/div[4]/div/div/div/div/div[2]/table/tbody/tr[{}]/td[3]'.format(j)
        city = driver.find_element_by_xpath(xpath2).text
        name_list.append(name)
        city_list.append(city)
    # flips the dimension of list to make them 15x1 instead of 1x15 arrays
    name_list = np.flip(name_list)
    city_list = np.flip(city_list)
    df = pd.DataFrame(name_list)
    df2 = pd.DataFrame(city_list)
    # concatenates new dataframes together
    new_df = pd.concat([df, df2], axis=1)
    csv_data = csv_data.append(new_df)

path = "xyz1-{}, {}{}.csv".format(num_pages, month, year)
csv_data.to_csv(path, index=False)



# close browser
driver.close()
# quit webdriver application
driver.quit()
