#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import pymongo
import requests


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser=init_browser()
    mars_dict={}

    #Nasa Mars News
    url='https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    #retrive latest news title and paragraph
    news_title = soup.find_all('div',class_='content_title')[1].text
    news_p = soup.find_all('div',class_='article_teaser_body')[0].text


    #JPL Mars Space Images
    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    time.sleep(1)
    html = browser.html
    images_soup = bs(html, 'html.parser')

    # Retrieve featured image link
    relative_image_path = images_soup.find_all('img')[3]["src"]
    featured_image_url = relative_image_path

    #Mars Facts
    facts_url='https://space-facts.com/mars/'
    tables=pd.read_html(facts_url)
    facts_df=tables[2]
    facts_df.columns=["Fact","Value"]
    mars_html=facts_df.to_html()
    mars_html.replace('\n','')

    #scrape Mars hemisphere name and Image 
    usgs_url = 'https://astrogeology.usgs.gov'
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(1)
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'html.parser')

    #Mars hemisphere data

    all_hemispheres = hemisphere_soup.find('div', class_='collapsible results')
    mars_hemisphere = all_hemispheres.find_all('div', class_='item')
    image_urls = []

    ## Iterate through each hemisphere data
    for i in mars_hemisphere:
        #collect title
        hemisphere=i.find('div',class_="description")
        title=hemisphere.h3.text

        #collect image link by browser to hemisphere page 
        hemisphere_link=hemisphere.a["href"]
        browser.visit(usgs_url + hemisphere_link)
        time.sleep(1)
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
    
        image_urls.append(image_dict)

    #create dic

    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_html),
        "hemisphere_images":image_urls
    }

    browser.quit()

    return mars_dict










    

