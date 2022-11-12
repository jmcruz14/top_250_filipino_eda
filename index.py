import pandas
import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import re
import requests
import time

letterboxd_main_url = 'https://letterboxd.com'

PATH = r'/Users/jccruz/Desktop/letterboxd_list_scraper/geckodriver'

options=Options()
options.add_argument("-headless")
browser = webdriver.Firefox(executable_path = PATH, keep_alive = False, options=options)
browser.implicitly_wait(15)
browser.get('https://letterboxd.com/scrimer/list/top-250-narrative-feature-length-filipino/')

#Scroll to center of page
browser.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
title = browser.title
soup_1 = BeautifulSoup(browser.page_source, 'lxml')

# data-target-link="/film/barbers-tales/" - href link

movie_titles = []

for div_info in soup_1.find_all('div', attrs={'class':'really-lazy-load'}):
    film_info = div_info.find('img')
    movie_titles.append(film_info.get('alt'))
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

print(title)
print(movie_titles)
print('list length:', len(movie_titles))

#soup = BeautifulSoup(page_source, 'lxml')