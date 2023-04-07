from list_class import *
from csv_writer import *
import re

'''
Letterboxd List scraper - main program
'''

def main():
    print('====================================================')
    print('Welcome to the Letterboxd List scraper!')
    print('Provided with an URL, this program outputs a CSV file') 
    print('of movie title, release data and Letterboxd link.') 
    print('Example url: (https://letterboxd.com/.../list/short-films/).')
    print('The program currently only supports lists and watchlists.')
    print('Enter q or quit to exit the program.')
    print('====================================================\n')
    
    # Checking if URL is of a watchlist or of a list
    while True:
        list_url = input('Enter the URL of the list you wish to scrape: ')

        ## 1.2 INCLUSION: add function to check which data to scrape:
        scrape_select = input("""\nType down which variables you'd like to scrape and separate with a ','.\n
            You can choose from the following data:\n
            - Film_title, Release_year, Runtime, Director, Producer\n
            - Writer, Editor, Cinematographer, Production_Design,\n
            - Composer, Sound, Genre, Cast, Personal_rating\n
            - Average_rating, Letterboxd_URL\n
            Sample input: Director, Producer, Release_year, Runtime\n
            Input (Leaving this blank will lead to the default option): """)
        try:    
            scrape_select_list = re.split(r',[\s]+', scrape_select)
            assert '' not in scrape_select_list
        except:
            scrape_select_list = ['Film_title', 'Release_year', 'Runtime', 'Average_rating', 'Letterboxd_URL']
        
        # dev note: if input = Director, Film_title,    (with trailing whitespaces) => exception raised
        # make fixes on this soon?
        
        ## END OF 1.2 CHANGES

        # exit option
        if list_url == 'q' or list_url == 'quit':
            exit()
            
        # if a watchlist proceed this way
        elif list_url.split('/')[-3] != 'list':
            try:
                list_name = list_url.split('/')[-2]
                username = list_url.split('/')[-3]
                current_list = List(list_name, list_url, selected_data=scrape_select_list)
                break

            except:
                print('That is not a valid URL, please try again.')
                continue
        
        # if a list proceed this way
        elif list_url.split('/')[-3] == 'list':
            try:
                list_name = list_url.split('/')[-2]
                current_list = List(list_name, list_url, selected_data=scrape_select_list)
                break

            except:
                print('That is not a valid URL, please try again.')
                continue
    
    # writing to a CSV file
    try:
        csv_name = username + '_' + list_name
        print(f'Writing to {csv_name}.csv.')
        list_to_csv(current_list.films, csv_name)
          
    except:
        print(f'Writing to {list_name}.csv.')
        list_to_csv(current_list.films, list_name)
    
    print('Done!')

if __name__ == "__main__":
    main()
