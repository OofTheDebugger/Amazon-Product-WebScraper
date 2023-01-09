import csv
from bs4 import BeautifulSoup
import subprocess

# Firefox and Chrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options

# Microsoft Edge
from msedge.selenium_tools import Edge, EdgeOptions


product = input("Enter a product to scrape: ")
product = product.lower()

# Firefox and Chrome 
#driver = webdriver.Firefox()
#driver = webdriver.Chrome(ChromeDriverManager().install())

# Edge
#options = EdgeOptions()
#options.use_chromium = True
#driver = Edge(options=options)

#Generates url for what you want to search

def get_url(search_term):
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')

    #adding query to url
    url = template.format(search_term)

    # page query place holder
    url += '&page={}'

    return url

""""
test

#record
item = results[0]
atag = item.h2.a
description = atag.text.strip()
url = 'https://www.amazon.com' + atag.get('href')

price_parent = item.find('span', 'a-price')
price = price_parent.find('span', 'a-offscreen').text

rating = item.i.text

review_count = item.find('span', {'class':'a-size-base', 'dir':'auto'}).text
"""

def extract_info(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    try:
        # product price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return
    
    try:
        # rating and review count
        rating = item.i.text
        print(rating)
        review_count = item.find('span', {'class': 'a-size-base s-underline-text'}).text
        print(review_count)
    except AttributeError:
        rating = ''
        review_count = ''
        
    result = (description, price, rating, review_count, url)
    
    return result



def main(search_term): 
    
    # Create ChromeOptions object
    chrome_options = Options()

    # Add the '--headless' flag
    chrome_options.add_argument('--headless')

    #startup web driver
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    # if you want to see the automation thats going on comment out ^ and remove the # to the next line
    #driver = webdriver.Chrome(ChromeDriverManager().install())

    storage = []
    url = get_url(search_term) 

    for page in range(1, 21):
        try:
            driver.get(url.format(page))
            #soup Object
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            results = soup.find_all('div', {'data-component-type':'s-search-result'})
            for item in results:
                info = extract_info(item)
                if info:
                    storage.append(info)
        except AttributeError:
            break
    driver.close()

    with open(f'{search_term} Products Results.csv', 'w', newline = '', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'Review Count', 'Url'])
        writer.writerows(storage)  

    print('Look in your folder! For your spreadsheet!!!')

main(product)
