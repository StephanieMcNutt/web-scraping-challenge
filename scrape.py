# Dependencies
import time
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
   
    # ---------NASA Mars News---------
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Retrieve the page
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Examine the results, then determine element that contains info. Results are returned as an iterable list
    news_titles = soup.find(class_='slide')
    # Wait 3 seconds to load the page
    time.sleep(3)
    # find the news title and body
    news_title = news_titles.find(class_='content_title').text
    news_p = news_titles.find(class_="article_teaser_body").text      
   
    # ---------Featured Image URL---------
    # URL of page to be scraped
    url="https://www.jpl.nasa.gov/images?search=&category=Mars"
    # Retrieve the page
    browser.visit(url)
    # Wait 3 seconds to load the page
    time.sleep(3)
    browser.links.find_by_partial_text('Image').click()
    # Wait 3 seconds to load the page
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list
    featured_image_url = soup.find('img', class_="BaseImage")['src']
    
    # ---------Mars Facts---------
    # target url
    url="https://space-facts.com/mars/"
    # pandas read the tables from a website to a list
    tables = pd.read_html(url)
    df=tables[0]
    mars_facts_table_df=df.rename(columns={0: "Characteristic", 1: "Value"})
    # add table content into a list of dictionaries
    mars_facts_table = mars_facts_table_df.to_dict('records')
    
    # --------Mars Hemispheres---------
    # URL of page to be scraped
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Retrieve the page
    browser.visit(url)
    # Wait 3 seconds to load the page
    time.sleep(3)
    #find the titles of the img and stores in a list
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    titles=soup.find_all('h3')
    titles[:]=(title.text for title in titles)
    titles[:]=(title.split(" Enhanced")[0] for title in titles)
    hemisphere_image_urls=[]
    for title in titles:
        browser.visit(url)
        browser.links.find_by_partial_text(title).click()
        time.sleep(3)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        # find the img_url
        img_url=soup.find('div',class_='downloads').ul.li.a['href']
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
    
    # Organized scraped data into one dictionary
    mars_scraped = {"news_title":news_title, "news_p":news_p,"featured_image_url":featured_image_url,"mars_facts_table":mars_facts_table,
                "hemisphere_image_urls":hemisphere_image_urls}
    
    browser.quit()
    
    return mars_scraped
    
    