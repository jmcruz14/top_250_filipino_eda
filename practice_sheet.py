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

url = 'https://skyscrapercity.com/threads/filipino-mentality-behavior-beliefs-traits-and-traditions.308931/'

PATH = r'/Users/jccruz/Desktop/letterboxd_list_scraper/geckodriver'

options=Options()
options.add_argument("-headless")
browser = webdriver.Firefox(executable_path = PATH, keep_alive = False, options=options)
browser.implicitly_wait(40)
browser.get(url)

titles = browser.find_elements(By.CLASS_NAME, 'title')
name = []
for title in titles:
    name.append(title.text)

print(name)