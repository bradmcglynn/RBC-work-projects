# Purpose of program: pull T4As from all yrs for all members (including deceased) from I&TS site
# will store temporarily in Group Operations folder, to reduce file size will zip files

import pandas as pd
import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import os
import time
# for regular expressions (RegEx), a sequence of characters that forms a search pattern
# can be used to check if a string contains the specified search pattern
import re
import shutil
from shutil import copyfile
from datetime import datetime
# to hide password input
from getpass import getpass

# PDF opens automatically in Chrome PDF Viewer w/o saving - want to bypass that and just download PDF w/o previewing it
# SIN csv to iterate through
def set_up_driver():
    #https://dbader.org/blog/python-parallel-computing-in-60-seconds#.
    search_data_df = pd.read_csv("Final Data List.csv",
                         encoding="latin-1", low_memory=False)



    directory = r"C:\Users\348834540\Downloads"
    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': directory, # Change default directory for downloads
        'download.prompt_for_download': False, # To auto download the file
        'download.directory_upgrade': True,
        'plugins.always_open_pdf_externally': True # It will not show PDF directly in chrome
    })

    # where chromedriver app is located; NOTE: as of Oct 29, 2021 RBC is using Chrome 94 - need to download again
    driver = webdriver.Chrome(r"chromedriver.exe", options=chrome_options)
    # get() method will navigate to a page given by URL
    listsURL = "url"
    driver.get(listsURL)
    enter_login_info(driver, search_data_df)

def enter_login_info(driver, search_data_df):
    # Find the username field by its id in the HTML markup - will look like [id="uid"]
    username = driver.find_element_by_id("j_username")
    password = driver.find_element_by_id("j_password")
    time.sleep(3)
    # ADD PAUSES BETWEEN STEPS
    # enter in your personal login info
    username.send_keys("abc")
    password.send_keys("xyz")
    time.sleep(3)
    # simulates pressing the login button
    # NEED TO ADD SOMETHING TO LOOP BACK IF I ENTER PASSWORD WRONG, like a pop-up screen that will erase my_password
    log_in_button = driver.find_element_by_xpath("/html/body/div/app-root/div/app-login-basic/div/main/"
                                                 "form/div/div/div[2]/button")
    log_in_button.click()

    time.sleep(30)
    home_page_handle = find_search_bar(driver)
    enter_info(driver, search_data_df, home_page_handle)
    exit_driver(driver)

def find_search_bar(driver):
    # record window handle of I&TS home page
    home_page_handle = driver.current_window_handle
    print(home_page_handle)
    # STEP ONE: Navigate to 'Benefit Payments'
    menu = driver.find_element_by_id('mainmenu_bp').click()
    # Click on 'Pensioner Information Inquiry'
    hidden_submenu = driver.find_element_by_id('link.bp.inquiry').click()
    time.sleep(5)
    return home_page_handle

def switch_driver_handle(driver):
    # record window handle of pensioner inquiry page
    driver.switch_to.window(driver.window_handles[1])
    pensioner_inquiry_handle = driver.current_window_handle
    print(pensioner_inquiry_handle)

    # switch frames to main
    return pensioner_inquiry_handle


def enter_info(driver, search_data_df, home_page_handle):
    # loops through all SIN values, inputting them and downloading their associated pdfs
    for i in range(0, len(search_data_df)):
        # switched to appropriate frame
        pensioner_inquiry_handle = switch_driver_handle(driver)
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="TopSM"]/frame[3]'))

        # refreshes page
        refresh_page(driver)
        pensioner_inquiry_handle = switch_driver_handle(driver)
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="TopSM"]/frame[3]'))

        time.sleep(3)
        print(driver.current_window_handle)
        time.sleep(3)
        send_info_to_keys(driver, search_data_df, i)
        time.sleep(3)
        click_search_button(driver)
        # results pop up, click member
        # will later need to insert loop here when looping thru many members
        testing = driver.find_element_by_xpath('//*[@id="dDet"]/table/tbody/tr[2]/td[1]/a')
        time.sleep(3)
        testing.click()
        function_caller(driver, home_page_handle, pensioner_inquiry_handle)
        print(driver.current_window_handle)

def send_info_to_keys(driver, search_data_df, i):
    # Navigate to 'SIN Number' search bar
    sin_tab = driver.find_element_by_xpath('//*[@id="SinNum"]')
    # Gets SIN from list, 'types' in search bar

    sin_tab.send_keys(search_data_df.iat[i, 2])
    # Navigate to 'Employee Number' search bar
    EENO_tab = driver.find_element_by_xpath('//*[@id="EmpNum"]')
    # Gets SIN from list, 'types' in search bar

    EENO_tab.send_keys(int(search_data_df.iat[i, 1]))

    # Navigate to 'Plan Number' search bar
    plan_tab = driver.find_element_by_xpath('//*[@id="PlanNum"]')
    # Gets SIN from list, 'types' in search bar

    plan_tab.send_keys(int(search_data_df.iat[i, 0]))


def click_search_button(driver):

    # 'clicks' search, NOTE: search results will still be in the same 'main' frame, so no need to switch
    search_button = driver.find_element_by_id('btnSearch')
    time.sleep(3)
    search_button.click()
    time.sleep(5)

def refresh_page(driver):
    driver.get(driver.current_url)
    time.sleep(3)
    driver.refresh()
    time.sleep(3)


def function_caller(driver, home_page_handle, pensioner_inquiry_handle):
    switch_driver_handles2(driver, home_page_handle, pensioner_inquiry_handle)
    #print_testing_info(driver)
    get_tax_info(driver)


def switch_driver_handles2(driver, home_page_handle, pensioner_inquiry_handle):
    # this opens a new window - need to switch handles again
    for handle in driver.window_handles:
        if (handle == home_page_handle) or (handle == pensioner_inquiry_handle):
            print(handle)
        else:
            member_handle = handle

    driver.switch_to.window(member_handle)



def print_testing_info(driver):
    # extract member name, EENO from page, is at top of page in 'first' frame
    driver.switch_to.frame('first')
    testing = driver.find_element_by_xpath('/html/body/table[2]').text
    print(testing)

    # extract number of rows and columns in 'first' frame table, to iterate later to extract member info
    num_rows = len(driver.find_elements_by_xpath('/html/body/table[2]/tbody/tr'))
    print(num_rows)
    num_cols = len(driver.find_elements_by_xpath('/html/body/table[2]/tbody/tr[1]/td'))
    print(num_cols)
    # xpath that when iterated over will be the xpath for every element in the table
    before_XPath = "/html/body/table[2]/tbody/tr["
    aftertd_XPath = "]/td["
    aftertr_XPath = "]"

    # print every element in the table
    for t_row in range(1, num_rows + 1):
        for t_column in range(1, num_cols + 1):
            FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
            cell_text = driver.find_element_by_xpath(FinalXPath).text
            print(cell_text)


def switch_to_tax_frame(driver):
    driver.switch_to.parent_frame()
    time.sleep(5)
    driver.switch_to.frame('Header')

    # click on 'Tax Forms' page
    tax_forms = driver.find_element_by_id('Ta525')
    tax_forms.click()

    # have to switch back to default/parent frame before switching to 'Main' frame
    driver.switch_to.parent_frame()
    time.sleep(5)
    # switch to 'Main' frame - this is where the tax form link is found
    driver.switch_to.frame('Main')
def get_tax_info(driver):
    # QUESTION: should we extract some extra member info to store in pandas DB?
    # In case we have to check over files and verify it's correct file for each member, especially in 'Personal' tab
    # switch to frame with all the member tabs


    # NOTE: some members have multiple T4As for a single tax year, due to premiums
    # click on PDF
    time.sleep(3)
    switch_to_tax_frame(driver)
    i = 0
    #tbody = driver.find_element_by_css_selector('#Ta > table:nth-child(3) > tbody')
    #for row in tbody.find_elements_by_xpath('./tr'):
        #i += 1

    for j in range(5, 12):

        pdf = driver.find_elements_by_xpath('//*[@id="Ta"]/table[2]/tbody/tr[{}]/td[10]'.format(i))
        print(pdf)
        pdf.click()


        #T4A = driver.find_element_by_xpath('//*[@id="Ta"]/table[2]/tbody/tr[{}]/td[10]/a'.format(i))

        #T4A.click()

# rename file - naming convention is EENO + name + year of tax form

# need to add try and except - what if 2+ records appear for EENO we thought was unique?
def exit_driver(driver):
    # close browser
    driver.close()
    # quit webdriver application
    driver.quit()


