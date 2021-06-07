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

    # delay to allow time for page to load
    time.sleep(5)

    # create beautifulsoup object
    article_soup = BeautifulSoup(browser.html, 'html.parser')
    article_result = article_soup.find('article')

    try:
        news_date = article_result.find('div', class_ = 'list_date').get_text()
        news_title = article_result.find('div', class_ = 'content_title').get_text()
        news_p = article_result.find('div', class_ = 'article_teaser_body').get_text()
    except:
        return None, None, None
    return news_date, news_title, news_p