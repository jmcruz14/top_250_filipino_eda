from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import numpy as np
from thefuzz import process

import re
from collections import defaultdict

_domain = 'https://letterboxd.com/'

## additional dev notes: insert a class function to activate specific methods?

def scrape_list(list_link, selected_data):
    """
    Takes in a Letterboxd link and outputs a list of film title, release year, 
    director, cast, average rating and letterboxd url
    """
    
    film_rows = []
    
    # Original formula
    #film_rows.append(['Film_title', 'Release_year', 'Director', 'Cast', 'Personal_rating', 'Average_rating','Letterboxd URL'])
    
    # Modified (V2)
    film_rows.append(['Film_title', 'Release_year', 'Runtime', 'Director',
                      'Producer', 'Writer', 'Editor', 'Cinematography', 'Production_Design',
                      'Composer', 'Sound', "Genre",
                      'Cast', 'Personal_rating', 'Average_rating','Letterboxd URL', "Services"])

    # plans for this code:
    # take the selected_data list, and match it with corresponding titles in film_rows column
    # if process.extract is < 80, the selected_data element is dropped
    # selected_data after it is checked with film_rows is used as basis for specific data to be extracted

    while True:
        list_page = requests.get(list_link)
        
        # check to see page was downloaded correctly
        if list_page.status_code != 200:
            encounter_error("")

        soup = BeautifulSoup(list_page.content, 'html.parser')
        # browser.get(following_url)
        
        # grab the main film grid
        table = soup.find('ul', class_='poster-list')
        if table is None:
            return None
        
        films = table.find_all('li')
        
        # iterate through films
        for film in tqdm(films):
            
            # finding the film name
            panel = film.find('div').find('img')
            film_name = panel['alt']
            
            # try to find the rating of a film if possible and converting to float
            try:
                stars = film.find('span', class_='rating').get_text().strip()
                rating = transform_stars(stars)
            except:
                rating = np.nan
            
            # Obtaining release year, director, cast and average rating of the movie
            film_card = film.find('div').get('data-target-link')
            film_page = _domain + film_card
            filmget = requests.get(film_page)
            # Parses the selected film in the list
            film_soup = BeautifulSoup(filmget.content, 'html.parser')
            
            # obtain meta tag for release_year and director
            release_year = film_soup.find('meta', attrs={'property':'og:title'}).attrs['content'][-5:-1]
            director = film_soup.find('meta', attrs={'name':'twitter:data1'}).attrs['content']
            
            # V2 UPDATES
            # exception handling for runtime
            try:
                runtime = int(re.sub(r"\D", '', film_soup.find('p', class_='text-link text-footer').get_text()))
            except:
                runtime = np.nan

            # exception handling for crew_members
            try:
                crew_tab = film_soup.find('div', {'id': 'tab-crew'})
                crew_labels = []
                crew_names = []

                for child in crew_tab.contents:
                    if child.name == 'h3':
                        crew_labels.append(child.find('span', {'class': 'crewrole -short'}).text)
                    if child.name == 'div':
                        crew_names.append([line.contents[0] for line in child.find_all('a')])
                
                # Dictionary a zip object of crew_tab
                crew_dict = dict(zip(crew_labels, crew_names))

                producer = crew_dict.get("Producer", crew_dict.get("Producers", np.nan))
                writer = crew_dict.get("Writer", crew_dict.get("Writers", np.nan))
                editor = crew_dict.get("Editor", crew_dict.get("Editors", np.nan))
                cinematography = crew_dict.get("Cinematography", crew_dict.get("Cinematography", np.nan))
                prod_design = crew_dict.get("Production Design", np.nan)
                composer = crew_dict.get("Composer", np.nan)
                sound = crew_dict.get("Sound", np.nan)

            except:
                producer = np.nan
                writer = np.nan
                editor = np.nan
                cinematography = np.nan
                prod_design = np.nan
                composer = np.nan
                sound = np.nan

            
            # exception handling for addtl details
            # studios / country / language

                ### COMING SOON

            # exception handling for genres
            try:
                #genre = [ line.contents[0] for line in film_soup.find('div', attrs={'id':'tab-genres'}).find_all('a')]

                genre_tab = film_soup.find('div', {'id': 'tab-genres'})
                genre_labels = []
                genre_types = []

                for child in genre_tab.contents:
                    if child.name == 'h3':
                        genre_labels.append(child.find('span').text)
                    if child.name == 'div':
                        genre_types.append([line.contents[0] for line in child.find_all('a')])
                
                genre_dict = dict(zip(genre_labels, genre_types))

                genre = genre_dict.get("Genres", genre_dict.get("Genre", np.nan))
            except:
                genre = np.nan

            # available services
            # CURRENTLY UNDER DEVELOPMENT
            try:
                # this parsing works
                # issue is on the html data that is scraped
                # the services available are most likely available via services
                watch_div = film_soup.find("div", {"id": "watch"})
                
                services = []

                if watch_div:
                    services_divs = watch_div.find_all(['section', 'div'], class_=['services', 'other'])
                    for services_div in services_divs:
                        services += [a.text.strip() for a in services_div.find_all('a') if a.text.strip()]

                # services = str(film_soup.find("div", {"id": "watch"}))
                # script_tag = film_soup.find('script', attrs={'type': 'application/ld+json'})
                # services = str(script_tag)

            except Exception as e:
                services = str(e)
                #services = np.nan

            #### END OF V2 UPDATES
            # try to find the cast, if not found insert a nan
            try:
                cast = [ line.contents[0] for line in film_soup.find('div', attrs={'id':'tab-cast'}).find_all('a')]
                
                # remove all the 'Show All...' tags if they are present
                cast = [i for i in cast if i != 'Show All…']
            
            except:
                cast = np.nan
            
            # try to find average rating, if not insert a nan
            try:
                average_rating = float(film_soup.find('meta', attrs={'name':'twitter:data2'}).attrs['content'][:4])
            except:
                average_rating = np.nan

            film_rows.append([film_name, release_year, runtime, director, 
                              producer, writer, editor, cinematography, prod_design,
                              composer, sound, genre,
                              cast, rating, average_rating, _domain+film_card, services])
            
        # check if there is another page of ratings
        next_button = soup.find('a', class_='next')
        if next_button is None:
            break
        else:
            list_link = _domain + next_button['href']
            
    return film_rows

def transform_stars(starstring):
    """
    Transforms star rating into float value
    """
    stars = {
        "★": 1,
        "★★": 2,
        "★★★": 3,
        "★★★★": 4,
        "★★★★★": 5,
        "½": 0.5,
        "★½": 1.5,
        "★★½": 2.5,
        "★★★½": 3.5,
        "★★★★½": 4.5
    }
    try:
        return stars[starstring]
    except:
        return np.nan

## FUNCTIONS WHICH ACTIVATE EACH SPECIFIC SCRAPING PROCESS
## V2 – to be used for the select function
def scrape_film_name(film_link):
    # finding the film name
    panel = film_link.find('div').find('img')
    film_name = panel['alt']

    return film_name

def scrape_film_rating(film_link):
    try:
        stars = film_link.find('span', class_='rating').get_text().strip()
        rating = transform_stars(stars)
    except:
        rating = np.nan
    return rating

## to be continued