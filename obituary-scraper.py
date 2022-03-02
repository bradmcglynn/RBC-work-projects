# Equifax Scraper Script
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



# where chromedriver app is located
driver = webdriver.Chrome(r"chromedriver.exe")

listsURL = "url"
    # get() method will navigate to a page given by URL
driver.get(listsURL)
    # allows page to load in properly
email = 'abc'
password = 'xyz'
driver.set_page_load_timeout(10)
driver.implicitly_wait(3)

email_prompt = driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/form/div/div[2]/span/input')
email_prompt.send_keys(email)

password_prompt = driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/form/div/div[3]/span/input[1]')
password_prompt.send_keys(password)

sign_in_prompt = driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/form/div/input')
sign_in_prompt.click()


csv_data = pd.read_csv("Obituary Keys 2022.csv", names=["Keys"])

name_list = []
DOB_list = []
DOD_list = []
last_address_list = []
obituary_list = []
data_publisher_list = []

for i in range(0, len(csv_data)):
    input = csv_data.iat[i,0]


    input_prompt = driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/form/div/span/input')
    input_prompt.clear()
    input_prompt.send_keys(input)

    driver.implicitly_wait(3)

    search_button = driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/form/input[1]')
    search_button.click()

    driver.set_page_load_timeout(10)
    driver.implicitly_wait(3)


    name_xpath = '/html/body/div/div[2]/div[2]/p[1]'
    name = driver.find_element_by_xpath(name_xpath).text

    DOB_xpath = '/html/body/div/div[2]/div[2]/p[3]/span[1]'
    try:
        DOB = driver.find_element_by_xpath(DOB_xpath).text
    except:
        DOB = None
    
    DOD_xpath = '/html/body/div/div[2]/div[2]/p[3]/span[2]'

    try:
        DOD= driver.find_element_by_xpath(DOD_xpath).text
    except:
        DOD = DOB
        DOB = None
    address_xpath = '/html/body/div/div[2]/div[2]/p[4]'
    address = driver.find_element_by_xpath(address_xpath).text
    
    obituary_xpath = '/html/body/div/div[2]/div[2]/p[5]'
    try:
        obituary = driver.find_element_by_xpath(obituary_xpath).text
    except:
        obituary = None
    
    publisher_xpath = '/html/body/div/div[2]/div[2]/p[6]'
    try:
        publisher = driver.find_element_by_xpath(publisher_xpath).text
    except:
        publisher = None
    
    name_list.append(name)
    DOB_list.append(DOB)
    DOD_list.append(DOD)
    last_address_list.append(address)
    obituary_list.append(obituary)
    data_publisher_list.append(publisher)


    # flips the dimension of list to make them 15x1 instead of 1x15 array 
name_list = np.flip(name_list)
DOB_list = np.flip(DOB_list)
DOD_list = np.flip(DOD_list)
last_address_list = np.flip(last_address_list)
obituary_list = np.flip(obituary_list)
data_publisher_list= np.flip(data_publisher_list)


df = pd.DataFrame(name_list)
df2 = pd.DataFrame(DOB_list)
df3= pd.DataFrame(DOD_list)
df4 = pd.DataFrame(last_address_list)
df5= pd.DataFrame(obituary_list)
df6 = pd.DataFrame(data_publisher_list)

final_df = pd.concat([df, df2, df3, df4, df5, df6], axis=1)


path = "JAN2022Obituaries.csv"
final_df.to_csv(path, sep=",", index=False)


# close browser
driver.close()
# quit webdriver application
driver.quit()
