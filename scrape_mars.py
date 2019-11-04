# Import Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser


def scrape_info():
    # Set executable path and browser for splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Save url as a variable
    url = "https://mars.nasa.gov/news/"

    # Visit url using splinter
    browser.visit(url)

    # Save browser contents in html as variable
    page = browser.html

    # Create and parse BeautifulSoup object
    soup = bs(page, "html.parser")

    # Collect latest news title
    news_title = soup.find("div", class_="content_title").text

    # Strip whitespace
    news_title = news_title.strip()

    # Collect corresponding paragraph text
    news_p = soup.find("div", class_="rollover_description_inner").text

    #Strip whitespace
    news_p = news_p.strip()

    # Visit url using splinter
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Find featured image
    featured_img = browser.find_by_css("article.carousel_item").first

    # Set base url to concatenate with image url
    base_url = "https://www.jpl.nasa.gov"

    # Select image reference from featured_img
    featured_image_url = featured_img["style"]

    # Split with " delimiter to remove extra text
    featured_image_url = featured_image_url.split('"')[1]

    # Concatenate with base url to get full url
    featured_image_url = f"{base_url}{featured_image_url}"

    # Save url as a variable
    url = "https://twitter.com/marswxreport?lang=en"

    # Visit url using splinter
    browser.visit(url)

    # Save html contents as a variable
    page = browser.html

    # Create and parse BeautifulSoup object
    soup = bs(page, "html.parser")

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

    # Quit browser session
    browser.quit()

    # Use pandas to scrape Mars facts website
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)[1]

    # Format dataframe
    tables = tables.rename(columns = {0: "Description", 1: "Value"})
    tables = tables.set_index("Description")

    # Convert to html
    html_table = tables.to_html()
    html_table

    # Save url as a variable
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    
    # Retrieve page with requests
    response = requests.get(url)

    # Create and parse BeautifulSoup object
    soup = bs(response.text, "html.parser")

    # Find all divs containing hemisphere image links
    link_list = soup.find_all("a", class_="itemLink")

    # Set base url used to create links
    base_url = "https://astropedia.astrogeology.usgs.gov/download"

    # Extract links from divs
    cerberus = f"{base_url}{link_list[0]['href'].replace('/search/map', '')}.tif/full.jpg"
    schiaparelli = f"{base_url}{link_list[1]['href'].replace('/search/map', '')}.tif/full.jpg"
    syrtis = f"{base_url}{link_list[2]['href'].replace('/search/map', '')}.tif/full.jpg"
    valles = f"{base_url}{link_list[3]['href'].replace('/search/map', '')}.tif/full.jpg"

    links = [cerberus, schiaparelli, syrtis, valles]
    titles = []

    # Loop through soup results to get titles for each hemishphere
    for item in link_list:
        title = item.find("img")
        title = title["alt"]
        title = title.replace(" Enhanced thumbnail", "")
        titles.append(title)

    # Create empty list to store dictionaries for each title and url
    hemisphere_image_urls = []

    # Loop through links and titles and add dictionaries to list
    for item in range(len(links)):
        hemisphere_image_urls.append({"title": titles[item], "url": links[item]})

    # Create dictionary for all Mars data
    mars_data = {"headline": news_title, "subhead": news_p, "featured": featured_image_url, "weather": mars_weather, "table": html_table, "hemispheres": hemisphere_image_urls}

    # Return results in a single dictionary
    return mars_data