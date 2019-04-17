# Import Dependencies

from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from flask import Flask

app = Flask(__name__)

def scrape():
    # Save url as a variable

    url = "https://mars.nasa.gov/news/"
    # Retrieve page with requests

    response = requests.get(url)

    # Create and parse BeautifulSoup object

    soup = bs(response.text, "html.parser")

    # Collect latest news title
    news_title = soup.find("div", class_="content_title").text

    # Strip whitespace
    news_title = news_title.strip()

    # Collect corresponding paragraph text
    news_p = soup.find("div", class_="rollover_description_inner").text

    #Strip whitespace
    news_p = news_p.strip()

    # Set executable path and browser for splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit url using splinter
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Find featured image
    featured_img = browser.find_by_css("a.button").first.click()

    # Navigate to full-size image
    featured_img = browser.find_link_by_text("more info     ").click()

    # Save link to full size image as a variable
    full_size = browser.find_by_css("img.main_image")
    featured_image_url = full_size["src"]

    # Quit browser session
    browser.quit()

    # Save url as a variable
    url = "https://twitter.com/marswxreport?lang=en"

    # Retrieve page with requests
    response = requests.get(url)

    # Create and parse BeautifulSoup object
    soup = bs(response.text, "html.parser")

    # Find latest mars weather and save as a variable
    # Link text needs to be removed, so do not include .text in find
    mars_weather = soup.find("p", class_="TweetTextSize")

    # Find unwanted link text
    remove_link = soup.find("a", class_="twitter-timeline-link u-hidden")

    # Extract link text from mars_weather
    remove_link.extract()

    # Convert to text and replace line breaks with spaces
    mars_weather = mars_weather.text
    mars_weather = mars_weather.replace("\n", " ")

    # Use pandas to scrape Mars facts website
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)

    # Save url as a variable

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Retrieve page with requests

    response = requests.get(url)

    # Create and parse BeautifulSoup object

    soup = bs(response.text, "html.parser")

    # Find all divs containing hemisphere image links
    link_list = soup.find_all("a", class_="itemLink")

    # Set base url used to create links
    base_url = "https://astrogeology.usgs.gov"

    # Extract links from divs
    cerberus = f"{base_url}{link_list[0]['href']}"
    schiaparelli = f"{base_url}{link_list[1]['href']}"
    syrtis = f"{base_url}{link_list[2]['href']}"
    valles = f"{base_url}{link_list[3]['href']}"

    links = [cerberus, schiaparelli, syrtis, valles]
    titles = []

    # Loop through soup results to get titles for each hemishphere
    for item in link_list:
        title = item.find("img")
        title = title["alt"]
        title = title.replace(" thumbnail", "")
        titles.append(title)

    # Zip title and links list to create dictionary
    hemisphere_image_urls = dict(zip(titles, links))

    # Return results in a single dictionary
    return {"headline": new_title, "subhead": news_p, "featured": featured_image_url, "weather": mars_weather, "table": tables, "hemispheres": hemisphere_image_urls}

if __name__=="__main__":
    print()