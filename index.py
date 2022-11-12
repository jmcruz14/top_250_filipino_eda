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

PATH = r'/Users/jccruz/Desktop/letterboxd_list_scraper/geckodriver'

options=Options()
options.add_argument("-headless")
browser = webdriver.Firefox(executable_path = PATH, keep_alive = False, options=options)
browser.implicitly_wait(20)
browser.get('https://letterboxd.com/scrimer/list/top-250-narrative-feature-length-filipino/')

title = browser.title
soup_1 = BeautifulSoup(browser.page_source, 'lxml')

# data-target-link="/film/barbers-tales/" - href link

movie_titles = []

for div_info in soup_1.find_all('div', attrs={'class':'really-lazy-load', 'data-linked':'linked'}):
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

browser.quit()

print(title)
print(movie_titles)

#soup = BeautifulSoup(page_source, 'lxml')