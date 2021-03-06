
# Dependencies
from bs4 import BeautifulSoup 
import requests
import pymongo
from splinter import Browser
import os
import pandas as pd

#C:/Users/lorib/Downloads/chromedriver_win32/chromedriver.exe

executable_path = {"executable_path": "./chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# Define database and collection
db = client.mars
collection = db.items

# URL of page to be scraped
url = 'https://mars.nasa.gov/news'
browser.visit(url)

# Retrieve page with the requests module
html = browser.html
#html.text

# Create BeautifulSoup object; parse with 'lxml'
soup = BeautifulSoup(html, 'lxml')
print(soup)


# # NASA Mars News

news = soup.find('div', class_='content_title').find('a').text
    #'a', target="_self")
print(news)

#Collect the latest News Title and Paragraph Text.
news_title = soup.find('div', class_='content_title').find('a').text
    #'a', target="_self")
print(news_title)

news_p = soup.find('div', class_='article_teaser_body').text
    #'a', target="_self")
print(news_p)


# # JPL Mars Space Images - Featured Image

# Example:
#featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'

#Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(featured_image_url)


#Make sure to find the image url to the full size .jpg image.
#Make sure to save a complete url string for this image.
html = browser.html
soup = BeautifulSoup(html, 'lxml')
img_url = soup.find("a", class_="fancybox")['data-fancybox-href']
print(img_url)

root = "https://www.jpl.nasa.gov"

fullURL = root+img_url
print(fullURL)


import shutil
response = requests.get(fullURL, stream=True)
with open('img.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)


# # Mars Weather

#Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
#Save the tweet text for the weather report as a variable called mars_weather.

# Example:
#mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'

mars_weather_url= "https://twitter.com/marswxreport?lang=en"
browser.visit(mars_weather_url)

html = browser.html
soup = BeautifulSoup(html, 'lxml')

tweet_url = soup.find("div", class_="js-tweet-text-container").find('p').text[:165]
print(tweet_url)


# # Mars Facts

#Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, 
#Mass, etc.
mars_facts='https://space-facts.com/mars/'
browser.visit(mars_facts)

tables = pd.read_html(mars_facts)

df = tables[0]
df

#Use Pandas to convert the data to a HTML table string.
html_table = df.to_html()
html_table

html_table.replace('\n', '')
df.to_html('table.html')


# # Mars Hemispheres

mars_hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(mars_hemi_url)


#You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
html = browser.html
soup = BeautifulSoup(html, 'lxml')

hemi_pic = soup.find_all("img", class_='thumb')
hemi_pic

#Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. 
#Use a Python dictionary to store the data using the keys img_url and title.
hemisphere_image_urls=[]


# main_ul 
root = 'https://astrogeology.usgs.gov'

for hemi in hemi_pic:

    title = hemi['alt']
#     print(title)
    picUrl = hemi['src']
#     print(picUrl)
    
#     # go to full image website 
#     browser.visit(root + picUrl)
    
#     # HTML Object of individual hemisphere
#     partImgHtml = browser.html
    
# # Parse HTML with Beautiful Soup for every individual hemisphere information website 
#     soup = BeautifulSoup(partImgHtml, 'lxml')
    
    # Retrieve full image source 
    imgUrl = root + picUrl
    
    # Append the retreived information into a list of dictionaries 
    hemisphere_image_urls.append({"title" : title, "img_url" : imgUrl})
    
# Display hemisphere_image_urls
    
print(hemisphere_image_urls)

#Append the dictionary with the image url string and the hemisphere title to a list. 
#This list will contain one dictionary for each hemisphere.



# Example:
#hemisphere_image_urls = [
#    {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#    {"title": "Cerberus Hemisphere", "img_url": "..."},
#    {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#    {"title": "Syrtis Major Hemisphere", "img_url": "..."},

