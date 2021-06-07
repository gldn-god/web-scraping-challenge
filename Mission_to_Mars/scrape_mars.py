# import dependencies
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
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


# Scrape Most Recent News
def news(browser):
    browser.visit('https://mars.nasa.gov/news/')
    time.sleep(3)

    article_soup = BeautifulSoup(browser.html, 'html.parser')
    article_result = article_soup.find('article')

    try:
        news_date = article_result.find('div', class_ = 'list_date').get_text()
        news_title = article_result.find('div', class_ = 'content_title').get_text()
        news_p = article_result.find('div', class_ = 'article_teaser_body').get_text()
    except:
        return None, None, None
    return news_date, news_title, news_p


# Scrape Featured Image
def featured(browser):
    browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')
    time.sleep(3)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(3)

    image_soup = BeautifulSoup(browser.html, 'html.parser')

    try:
        image_result = image_soup.find(class_ = 'fancybox-image')['src']
    except:
        return None
    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_result}'
    return featured_image_url


# Scrape Facts Table
def facts(browser):
    browser.visit('https://space-facts.com/mars/')
    time.sleep(3)

    fact_soup = BeautifulSoup(browser.html, 'html.parser')
    try:
        fact_df = pd.read_html('https://space-facts.com/mars/')[0]
    except:
        return None
    
    fact_df.columns = ['Description', 'Mars']
    fact_df.set_index('Description', inplace = True)
    fact_html = fact_df.to_html(index = False, header = False)
    return fact_html