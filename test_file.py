from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Replace the URL below with the URL of the Letterboxd list you want to scrape
url = 'https://letterboxd.com/tuesjays/list/top-250-narrative-feature-length-filipino/'

PATH = r'/Users/jccruz/Desktop/letterboxd_list_scraper/geckodriver'

# Use the Firefox webdriver with headless mode to run in the background
options = FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(executable_path = PATH, keep_alive = False, options=options)

# Wait for up to 10 seconds for the page to fully load
driver.wait = WebDriverWait(driver, 10)

# Load the page and wait for it to fully load
driver.get(url)

# Scroll down to the bottom of the page to load more content
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

driver.wait.until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'js-list-entries poster-list -p125 -grid film-list')]")))

# Pass the page source to BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'lxml')

# Extract film list only
films_list = soup.find('ul', {'class':'js-list-entries'})

for poster in films_list:
    film = poster.find('div')
    print(film)

# Find all the film items in the list
films = soup.find_all('li', {'class': 'js-list-entries poster-list -p125 -grid film-list'})

for film in films:
    # Get the film title
    title = film.find('a', {'class': 'film-title'}).text.strip()

    # Get the film year
    year = film.find('span', {'class': 'year'}).text.strip()

    # Get the film director
    director = film.find('span', {'class': 'directed-by'}).find('a').text.strip()

    # Get the film actors
    actors = [a.text.strip() for a in film.find('span', {'class': 'starring'}).find_all('a')]

    # Get the film description
    description = film.find('div', {'class': 'film-list-description'}).text.strip()

    print('Title:', title)
    print('Year:', year)
    print('Director:', director)
    print('Actors:', actors)
    print('Description:', description)
    print('---')

# Close the webdriver
driver.quit()
