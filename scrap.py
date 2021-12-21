import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import openpyxl
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import math


TIMEOUT = 10

class ProductScraper():
    def __init__(self):
        self.base_url = "https://www.radiopopular.pt/pesquisa/"
    def load(self, filename):
        book = openpyxl.load_workbook(filename)
        sheet = book.active
        rows = sheet.rows
        productId= []
        for row in rows:
            productId.append(row[4].value)
        return productId
                
    def scrape(self):
        # write csv headers
        if os.path.exists('result.csv'):
            os.remove('result.csv')
        columns=['Id', 'Price']
        df = pd.DataFrame(columns = columns)
        df.to_csv('result.csv', mode='x', index=False, encoding='utf-8')

        # get products ids
        productIds= self.load('Out.xlsx')
        # scrap prices
        index= 0
        for productId in productIds:
            if index== 0:
                index+= 1
                continue
            try:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument(f"--window-size=1920, 900")
                chrome_options.add_argument("--hide-scrollbars")
                driver = webdriver.Chrome(options=chrome_options)
                driver.get(self.base_url+ str(productId))
                time.sleep(TIMEOUT)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
            except:
                print("Can't access this url!")
                return 0
            try:
                tmp= soup.find('div', attrs= {'class': 'price notranslate fl'})
                price= tmp.text
            except:
                price= 'None'
            new= {'Id': productId, 'Price': price}
            items= []
            items.append(new)
            df = pd.DataFrame(items, columns = columns)
            df.to_csv('result.csv', mode='a', header=False, index=False, encoding='utf-8')
if __name__ == '__main__':
    scraper = ProductScraper()
    scraper.scrape()