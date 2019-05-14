# Dependencies
from bs4 import BeautifulSoup 
import requests
import pymongo
from splinter import Browser
import os
import pandas as pd
import shutil
import datetime as dt


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017/marsdb'
client = pymongo.MongoClient(conn)


# Define database and collection

db = client.marsdb
collection = db.items
def scrape():
    browser=init_browser()

    #news title and news p
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find('div', class_='content_title').find('a').text
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    #featured image
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
    #Make sure to save a complete url string for this image.
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    img_url = soup.find("a", class_="fancybox")['data-fancybox-href']
    root = "https://www.jpl.nasa.gov"
    fullURL = root+img_url

    #Mars weather
    mars_weather_url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    tweet_url = soup.find("div", class_="js-tweet-text-container").find('p').text[:165]
   
    #Mars facts
    mars_facts='https://space-facts.com/mars/'
    browser.visit(mars_facts)
    tables = pd.read_html(mars_facts)
    df = tables[0]
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')

    #Mars Hemispheres
    mars_hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    hemi_pic = soup.find_all("img", class_='thumb')
    hemisphere_image_urls=[]
    # main_ul 
    root = 'https://astrogeology.usgs.gov'
    for hemi in hemi_pic:
        title = hemi['alt']
        picUrl = hemi['src']
        imgUrl = root + picUrl
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : imgUrl})
    


    # Close the browser after scraping
    browser.quit()

    #prepare data for insert
    marsdata = {
       "news_title": news_title,
       "news_paragraph": news_p,
       "featured_image": fullURL,
       "weather_tweet": tweet_url,
       "mars_facts": html_table,
       "hemisphers": hemisphere_image_urls,
       "last_modified": dt.datetime.now()
    }
    #insert
    #collection.update({}, marsdata, upsert=True)

    return marsdata