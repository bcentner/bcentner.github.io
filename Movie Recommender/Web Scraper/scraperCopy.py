import bs4
import requests
from dateutil.parser import parse
import concurrent.futures
import pandas as pd
import numpy as np

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
from dataclasses import dataclass

#FIRST PASTE BEGIN#

# Maximum number of threads that will be spawned
MAX_THREADS = 50
movie_title_arr = []
movie_year_arr = []
movie_genre_arr = []
movie_synopsis_arr =[]
image_url_arr  = []
image_id_arr = []

def getMovieTitle(header):
    try:
        return header[0].find("a").getText()
    except:
        return 'NA'

def getReleaseYear(header):
    try:
        return header[0].find("span",  {"class": "lister-item-year text-muted unbold"}).getText()
    except:
        return 'NA'

def getGenre(muted_text):
    try:
        return muted_text.find("span",  {"class":  "genre"}).getText()
    except:
        return 'NA'

def getsynopsys(movie):
    try:
        return movie.find_all("p", {"class":  "text-muted"})[1].getText()
    except:
        return 'NA'

def getImage(image):
    try:
        return image.get('loadlate')
    except:
        return 'NA'

def getImageId(image):
    try:
        return image.get('data-tconst')
    except:
        return 'NA'

    #END FIRST PASTE#

    #SECOND PASTE BEGIN#

    # An array to store all the URL that are being queried
imageArr = []

# Maximum number of pages one wants to iterate over
MAX_PAGE =51

# Loop to generate all the URLS.
for i in range(0,MAX_PAGE):
    totalRecords = 0 if i==0 else (250*i)+1
    print(totalRecords)
    imdb_url = f'https://www.imdb.com/search/title/?release_date=2020-01-02,2021-02-01&user_rating=9.0,10.0&languages=en&count=250&start={totalRecords}&ref_=adv_nxt'
    imageArr.append(imdb_url)

def download_stories(story_urls):
    threads = min(MAX_THREADS, len(story_urls))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(main, story_urls)

    #END SECOND PASTE#




def main(imdb_url):
    response = requests.get(imdb_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Movie Name
    movies_list  = soup.find_all("div", {"class": "lister-item mode-advanced"})
    
    for movie in movies_list:
        header = movie.find_all("h3", {"class":  "lister-item-header"})
        muted_text = movie.find_all("p", {"class":  "text-muted"})[0]
        imageDiv =  movie.find("div", {"class": "lister-item-image float-left"})
        image = imageDiv.find("img", "loadlate")
        
        #  Movie Title
        movie_title =  getMovieTitle(header)
        movie_title_arr.append(movie_title)
        
        #  Movie release year
        year = getReleaseYear(header)
        movie_year_arr.append(year)
        
        #  Genre  of movie
        genre = getGenre(muted_text)
        movie_genre_arr.append(genre)
        
        # Movie Synopsys
        synopsis = getsynopsys(movie)
        movie_synopsis_arr.append(synopsis)
        
        #  Image attributes
        img_url = getImage(image)
        image_url_arr.append(img_url)
        
        image_id = image.get('data-tconst')
        image_id_arr.append(image_id)


        # Call the download function with the array of URLS called imageArr
        download_stories(imageArr)

        # Attach all the data to the pandas dataframe. You can optionally write it to a CSV file as well
        movieDf = pd.DataFrame({
            "Title": movie_title_arr,
            "Release_Year": movie_year_arr,
            "Genre": movie_genre_arr,
            "Synopsis": movie_synopsis_arr,
            "image_url": image_url_arr,
            "image_id": image_id_arr,
        })

        print('--------- Download Complete CSV Formed --------')

        movie.to_csv('file.csv', index=False) #: If you want to store the file.
        movieDf.head()