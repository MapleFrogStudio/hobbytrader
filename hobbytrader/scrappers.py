# Scrapper is a module to scrape different websites that contain stock tickers 
# for different companies and excahnges.
# Functions return a dataframe with at least two columns [Symbol, Name]
# Other columns are available depending on website
#
# ADVFN : https://ca.advfn.com/investing/stocks
# FMP : https://site.financialmodelingprep.com/developer/docs/

import os
import json
import io
import re
import string
import time
import pandas as pd
import requests
import numpy as np
from urllib.request import urlopen
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from abc import ABC, abstractmethod
from urllib.request import urlopen

from hobbytrader import FMPAD_API_KEY

#from dotenv import load_dotenv

#load_dotenv()


class Scrapper(ABC):
    @abstractmethod
    def scrape_data(self):
        pass                                        # pragma: no cover (skip line from coverage test package)


class ADVFN(Scrapper):
    def __init__(self, exchange='tsx', country='canada') -> None:
        self.exchange = exchange
        self.country = country
        self.url_base = f'https://advfn.com/investing/stocks/{self.country}/{self.exchange}?letter='
        self.HEADER = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }  
        self.yahoo_suffix = {
            'tsx'    : '.TO',
            'tsxv'   : '.V',
            'nasdaq' : ''
        }

    
    def letters_list(self) -> list:
        """ Build letters and numbers list to loop in web site url path """
        letters = list(string.ascii_uppercase)
        letters.append('0')
        return letters

    def extract_all_lines_with_symbol_info(self, full_url) -> list:
        """ Extract all symbol data tags ('investing-list') and 'a' tags """
        html_text = requests.get(full_url, headers=self.HEADER).text
        soup = BeautifulSoup(html_text, 'html.parser')
        ul_tags = soup.find_all('ul', class_='investing-list')

        a_tags = []
        for ul in ul_tags:
            a_tags += ul.find_all('a')

        return a_tags
    
    def extract_name_and_symbol(self, html_tag) -> dict:
        """ html_tag is a beautiful soup tag element """
        name = html_tag.text
        name = name[:name.index('(')]  # Extract string up to first '('

        ticker = html_tag.text
        ticker = ticker[ticker.index('(')+1 : ticker.index(')') ]

        url = html_tag['href']
        symbol_info = {"Symbol":ticker, "Name":name, "Url":url}
        return symbol_info

    def scrape_data(self):
        letters = self.letters_list()

        symbols_list = []
        for letter in letters:
            full_url = f'{self.url_base}{letter}'
            print(full_url)
            
            a_tags = self.extract_all_lines_with_symbol_info(full_url)
            for a_tag in a_tags:
                symbol_info = self.extract_name_and_symbol(a_tag)
                symbols_list.append(symbol_info)
                #time.sleep(1)

        symbols_df = pd.DataFrame(symbols_list)
        return symbols_df

    def add_yahoo_symbol(self, symbols_df):
        suffix = self.yahoo_suffix[self.exchange]
        symbols_df['Yahoo'] = [f"{s.replace('.', '-')}{suffix}" for s in symbols_df.Symbol]
        return symbols_df

    def to_csv(self, symbols_df):
        symbols_df.to_csv(f'advfn-{self.exchange}.csv', index=False)

    def scrape_and_save_to_csv(self):
        symbols = s.scrape_data()                   # pragma: no cover (skip line from coverage test package)
        symbols = s.add_yahoo_symbol(symbols)       # pragma: no cover (skip line from coverage test package)
        s.to_csv(symbols)                           # pragma: no cover (skip line from coverage test package)

class FMPAD(Scrapper):
    def __init__(self, exchange='TSX') -> None:
        #self.api_key = os.getenv('FMPAD_API_KEY')
        self.api_key = FMPAD_API_KEY
        FMPAD_API_KEY
        self.exchange = exchange
        self.url_base = f'https://financialmodelingprep.com/api/v3/stock-screener?apikey={self.api_key}&exchange='
        print(self.api_key)

    def rename_columns(self, data_df):
        data_df.rename(columns={
                        "symbol": "Symbol", 
                        "companyName": "Name",
                        "marketCap": "MarketCap",
                        "sector": "Sector",
                        "industry": "Industry",
                        "beta": "Beta",
                        "price": "Price",
                        "lastAnnualDividend": "LastAnnualDividend",
                        "volume": "Volume",
                        "exchange": "Exchange",
                        "exchangeShortName": "ExchangeShortName",
                        "country": "Country",
                        "isEtf": "IsEtf",
                        "isActivelyTrading": "IsActivelyTrading"
                        }, inplace=True)
        return data_df

    def get_jsonparsed_data(self):
        response = urlopen(self.url_base + self.exchange)
        data = response.read().decode("utf-8")
        data_df = pd.DataFrame(json.loads(data))
        data_df = self.rename_columns(data_df)
        return data_df

    def scrape_data(self):
        data_df = self.get_jsonparsed_data()
        data_df = self.rename_columns(data_df)
        data_df['Yahoo'] = data_df.Symbol
        return data_df

if __name__ == '__main__':
    s = ADVFN(exchange='nasdaq', country='canada')  # pragma: no cover (skip line from coverage test package)
    s.scrape_and_save_to_csv()                      # pragma: no cover (skip line from coverage test package)