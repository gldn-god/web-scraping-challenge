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
    mars_data = {}
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    collection = db.articles

    # Scrape Most Recent News Headline
    browser.visit('https://mars.nasa.gov/news/')
    article_soup = soup(browser.html, 'html.parser')
    time.sleep(5)

    article_result = article_soup.find('article')
    news_date = article_result.find('div', class_ = 'list_date').text.strip()
    news_title = article_result.find('div', class_ = 'content_title').text.strip()
    news_p = article_result.find('div', class_ = 'article_teaser_body').text.strip()

    # Scrape Featured Web Image
    browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')
    browser.links.find_by_partial_text('FULL IMAGE').click()
    image_soup = soup(browser.html, 'html.parser')
    time.sleep(5)

    image_result = image_soup.find(class_ = 'fancybox-image')['src']
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image_result

    # Scrape Mars Facts
    browser.visit('https://space-facts.com/mars/')
    fact_soup = soup(browser.html, 'html.parser')
    time.sleep(5)

    fact_df = pd.read_html('https://space-facts.com/mars/')[0]
    fact_html = fact_df.to_html(index = False, header = False)

    # Scrape Hemispheres Images & URLs
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    hemi_soup = soup(browser.html, 'html.parser')
    time.sleep(5)

    hemisphere_content = hemi_soup.find_all('div', class_ = 'item')

    hemisphere_images = []

    for hemisphere in hemisphere_content:
        hemi_url = {}
    
        title = hemisphere.find('div', class_='description').h3.text
        hemi_url['title'] = title
        time.sleep(1)

        browser.find_by_text(title).click()
        hemi_soup = soup(browser.html, 'html.parser')
    
        download = hemi_soup.find('div', class_ = "downloads")
        src = download.find('a')
        if src.text == 'Sample':
            img_url = src['href']
            hemi_url['img_url'] = img_url
    
        hemisphere_images.append(hemi_url)
        time.sleep(1)
        browser.back()
    
    # Close Browser
    browser.quit()
