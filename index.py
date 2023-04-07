import pandas
import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import requests
import time

letterboxd_main_url = 'https://letterboxd.com'
letterboxd_list_url = 'https://letterboxd.com/tuesjays/list/top-250-narrative-feature-length-filipino/'

PATH = r'/Users/jccruz/Desktop/letterboxd_list_scraper/geckodriver'

options = Options()
options.add_argument("-headless")
browser = webdriver.Firefox(executable_path = PATH, keep_alive = False, options=options)
browser.implicitly_wait(40)
browser.get(letterboxd_list_url)

# Scroll to center of page
browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
title = browser.title

# Extract Page Source
soup_1 = BeautifulSoup(browser.page_source, 'lxml')

# data-target-link="/film/barbers-tales/" - href link

movie_titles_soup = []
movie_titles_selenium = []

# XPath to locate for div element to extract
# movie_div_xpath = "//div[contains(@class, 'poster film-poster')]"

#movie_list = soup_1.find_all('div', attrs={'data-image-width':'125'})

# Obtain Individual 
movie_list = soup_1.select('ul li div', limit=100)
print('movie list length', len(movie_list))
#print(movie_list)

for div_info in movie_list:
        #film_info = div_info.find('img')
            movie_titles_soup.append(div_info.find('img').get('alt'))

# insert for loop going through each page
# for page in range(3):
#     if page == 0:
#         browser.implicitly_wait(20)
#         for div_info in movie_list:
#         #film_info = div_info.find('img')
#             movie_titles_soup.append(div_info.find('img').get('alt'))
#         # print(div_info.find('img'))
#         # print(div_info.find('img').get('alt'))
#     else:
#         browser.get(letterboxd_list_url + 'page/' + str(page+1) + '/')
#         browser.implicitly_wait(20)
#         movie_list = soup_1.select('ul li div')
#         movie_list = movie_list[:100]
#         for div_info in movie_list:
#             movie_titles_soup.append(div_info.find('img').get('alt'))
#         browser.back()
#         continue

# Currently, the code produces 75 movies maximum
#         
movie_titles_soup = list(dict.fromkeys(movie_titles_soup)) # Remove duplicates

# WebDriverWait(browser, 20)

a_links = []

# Append succeeding links to another page
links_page = soup_1.find_all('li', attrs={'class':'paginate-page'})
for link in links_page:
    x = link.find('a')
    if x:
        x = link.find('a').get('href')
        a_links.append(x)
    else:
        a_links.append("None")

a_links.remove("None")

for href in a_links:
    href_addtl = letterboxd_main_url + href
    browser.get(href_addtl)
    print(href_addtl)
    # soup_2 = BeautifulSoup(browser.page_source, 'html.parser')
    # # WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'div')))
    # movie_list_new = soup_2.select('ul li div', limit=100)
    # for div_info in movie_list_new:
    #     #film_info = div_info.find('img')
    #         movie_titles_soup.append(div_info.find('img').get('alt'))
    

print(links_page)
print(a_links)

# for div_info in soup_1.find_all('div', attrs={'class':'really-lazy-load'}):
#     film_info = div_info.find('img')
#     movie_titles_soup.append(film_info.get('alt'))

# numbers = browser.find_elements(By.XPATH, movie_div_xpath)

# for number in numbers:
#     img_div = number.find_element(By.CSS_SELECTOR, 'img')
#     for i in range(4):
#         try:
#                 run_test = WebDriverWait(number, 120).until( \
#                 EC.presence_of_element_located((By.XPATH, "xpath")))
#                 run_test.click()
#                 break
#         except StaleElementReferenceException as e:
#                 raise e

#     print(img_div.get_attribute('alt'))
#     movie_titles_selenium.append(img_div.get_attribute('alt'))

# numbers = browser.find_elements(By.CLASS_NAME, 'poster-container')

# number_list = []
# movie_titles = []

# for number in numbers:
#     number_list.append(number.text)

#     number.click()

#     film_page = BeautifulSoup(number.page_source, 'lxml')

#     number.back()

# f = open('page_file.txt', 'w')
# f.write(str(soup_1))
# f.close()

browser.quit()

def parse_page():
    for div_info in movie_list:
        #film_info = div_info.find('img')
            movie_titles_soup.append(div_info.find('img').get('alt'))

print(title)
print(movie_titles_soup)
print('list length:', len(movie_titles_soup))

#soup = BeautifulSoup(page_source, 'lxml')