from list_scraper import *

class List:
    """
    List to store data pertaining to a specific list    
    """
    
    def __init__(self, list_name, link, selected_data=['Film_title', 'Release_year', 'Runtime', 'Average_rating', 'Letterboxd_URL']):
        """
        :param list_name: List name for data file (if applicable):
        :param link: The link of the list
        """
        
        self.name = list_name
        self.link = link
        self.selected_data = selected_data
        #print("\nScraping list data...\n")
        print(F'\nScraping list data for {self.selected_data}...\n')
        self.films = scrape_list(self.link, self.selected_data)