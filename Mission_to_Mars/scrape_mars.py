# import dependencies
from bs4 import BeautifulSoup as soup
import pandas as pd
from pprint import pprint
import pymongo
from splinter import Browser
import time

# initiate browser with chromedriver (Chrome v91)
def init_browser():
    executable_path = {'executable_path' : 'chromedriver'}
    browser = Browser(
        'chrome', 
        **executable_path, 
        headless = False
    )

# Scrape Mars Data
def mars_scrape():
    browser = init_browser()

    # MongoDB Setup
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client.mars_db
    collection = db.articles


    # Scrape Most Recent News Headline
    browser.visit('https://mars.nasa.gov/news/')
    time.sleep(3)
    article_soup = soup(browser.html, 'html.parser')

    article_result = article_soup.find('article')
    news_date = article_result.find('div', class_ = 'list_date').text.strip()
    news_title = article_result.find('div', class_ = 'content_title').text.strip()
    news_p = article_result.find('div', class_ = 'article_teaser_body').text.strip()

    recent_news = {
    'date' : news_date,
    'title' : news_title,
    'teaser' : news_p
    }


    # Scrape Featured Web Image
    browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')
    time.sleep(3)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(3)

    image_soup = soup(browser.html, 'html.parser')
    image_result = image_soup.find(class_ = 'fancybox-image')['src']
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image_result

    featured_image = {
        'featured_image_url' : featured_image_url
    }


    # Scrape Mars Facts
    browser.visit('https://space-facts.com/mars/')
    time.sleep(3)

    fact_soup = soup(browser.html, 'html.parser')
    fact_df = pd.read_html('https://space-facts.com/mars/')[0]
    fact_html = fact_df.to_html(index = False, header = False)

    facts = {
        'html_table' : fact_html
    }


    # Scrape Hemispheres Images & URLs
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    time.sleep(3)

    hemi_soup = soup(browser.html, 'html.parser')
    hemisphere_content = hemi_soup.find_all('div', class_ = 'item')
    hemispheres = {}

    for hemisphere in hemisphere_content:
        hemi_name = hemisphere.find('div', class_='description').h3.text
        browser.find_by_text(hemi_name).click()
        time.sleep(3)
        hemi_soup = soup(browser.html, 'html.parser')
        download = hemi_soup.find('div', class_ = "downloads")
        src = download.find('a')
        if src.text == 'Sample':
            hemi_url = src['href']
        hemispheres[hemi_name] = hemi_url
        browser.back()
        time.sleep(1)


    # Close Browser
    browser.quit()


    # Import to MongoDB
    collection.delete_many({})
    collection.insert_many([recent_news, featured_image, facts, hemispheres])