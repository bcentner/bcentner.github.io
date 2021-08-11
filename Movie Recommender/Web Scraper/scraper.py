import bs4
import numpy as np

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


myUrl = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
# Opens connection, downloads page, and then closes connection
uClient = uReq(myUrl)
pageHtml = uClient.read()
uClient.close()

pageSoup = soup(pageHtml, "html.parser")
listHtml = pageSoup.findAll("tbody", {"class" : "lister-list"})
#print(listHtml)


titles = pageSoup.find_all("td", {"class" : "titleColumn"})
ratingInfo = pageSoup.find_all("td", {"class" : "rating column imdbRating"})
imgInfo = pageSoup.find_all("td", {"class", "posterColumn"})
#print(titles[0])