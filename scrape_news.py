# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd
import fnmatch


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    # Collecting the latest Tweets from Twitter with hashatag #foodallergy and US_FDA account tag
    news_url = 'https://twitter.com/search?q=%40US_FDA%20%23foodallergy&src=typd'
    browser.visit(news_url)
    # Storing the latest news title and paragraph text in variables
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'html.parser')
    twitter_handles = news_soup.find_all('a', class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")
    fa_texts = news_soup.find_all('p', class_="TweetTextSize js-tweet-text tweet-text")
    listings["food_allergy_news"] = []
    for handle in fa_texts:
        listings["food_allergy_news"].append(handle.text)
    
    return listings
