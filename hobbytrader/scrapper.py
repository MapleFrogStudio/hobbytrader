
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

load_dotenv()

#
# Scrapper is a module to scarpe different websites that contains stock tickers for different companies
# and excahnges.
# Functions return a dataframe with at least two columns [Symbol, Name]
# Other columns are available depending on website
#
# ADVFN : https://ca.advfn.com/investing/stocks
# FMP : https://site.financialmodelingprep.com/developer/docs/

def scrape_advfn(exchange='tsx', country='canada'):
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }    
    url_base = f'https://advfn.com/investing/stocks/{country}/{exchange}?letter='
    letters = list(string.ascii_uppercase)
    letters.append('0')
    #pattern = r'TSX\/(.*?)\/stock-price' # Extract symbol from url
    pattern = fr'{exchange.upper()}\/(.*?)\/stock-price' # Extract symbol from url

    symbols_list = []
    for letter in letters:
        full_url = f'{url_base}{letter}'
        print(full_url)
        html_text = requests.get(full_url, headers=header).text
        soup = BeautifulSoup(html_text, 'html.parser')
        ul_tags = soup.find_all('ul', class_='investing-list')

        a_tags = []
        for ul in ul_tags:
            a_tags += ul.find_all('a')
        
        for a_tag in a_tags:
            name = a_tag.text
            name = name[:name.index('(')]
            url = a_tag['href']
            ticker = re.findall(pattern, url)[0]
            symbol_info = {"Symbol":ticker, "Name":name, "Url":url}
            symbols_list.append(symbol_info)

        #time.sleep(1)

    symbols_df = pd.DataFrame(symbols_list)
    return symbols_df

#
# Predefined scrapper calls to use in github actions without parameters
#
def scrape_tsx_from_advfn():
    exchange = 'tsx'
    country = 'canada'
    symbols_df = scrape_advfn(exchange, country)
    symbols_df['Yahoo'] = [f"{s.replace('.', '-')}.TO" for s in symbols_df.Symbol]
    symbols_df = symbols_df[['Symbol','Yahoo','Name','Url']]
    symbols_df.to_csv(f'advfn-{exchange}.csv', index=False)


def scrape_tsxv_from_advfn():
    exchange = 'tsxv'
    country = 'canada'    
    symbols_df = scrape_advfn(exchange, country)
    symbols_df['Yahoo'] = [f"{s.replace('.', '-')}.V" for s in symbols_df.Symbol]
    symbols_df = symbols_df[['Symbol','Yahoo','Name','Url']]
    symbols_df.to_csv(f'advfn-{exchange}.csv', index=False)


def scrape_nasdaq_from_advfn():
    exchange = 'nasdaq'
    country = 'usa'    
    symbols_df = scrape_advfn(exchange, country)
    symbols_df['Yahoo'] = [f"{s.replace('.', '-')}" for s in symbols_df.Symbol]
    symbols_df = symbols_df[['Symbol','Yahoo','Name','Url']]
    symbols_df.to_csv(f'advfn-{exchange}.csv', index=False)
    return symbols_df

def scrape_nyse_from_advfn():
    exchange = 'nyse'
    country = 'usa'        
    symbols_df = scrape_advfn(exchange, country)
    symbols_df['Yahoo'] = [f"{s.replace('.', '-')}" for s in symbols_df.Symbol]
    symbols_df = symbols_df[['Symbol','Yahoo','Name','Url']]
    symbols_df.to_csv(f'advfn-{exchange}.csv', index=False)
    return symbols_df

def scrape_amex_from_advfn():
    exchange = 'amex'
    country = 'usa'        
    symbols_df = scrape_advfn(exchange, country)
    symbols_df['Yahoo'] = [f"{s.replace('.', '-')}" for s in symbols_df.Symbol]
    symbols_df = symbols_df[['Symbol','Yahoo','Name','Url']]
    symbols_df.to_csv(f'advfn-{exchange}.csv', index=False)
    return symbols_df

def scrape_fmp():
    api_key = os.getenv('FMPAD_API_KEY')
    #url = f'https://financialmodelingprep.com/api/v3/stock-screener?exchange={exchange}&apikey={api_key}'
    url = f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={api_key}'
    response = urlopen(url)
    data = response.read().decode("utf-8")
    data_df = pd.DataFrame(json.loads(data))
    data_df = data_df.rename(columns={"symbol": "Symbol", "name": "Name"})
    data_df.to_csv('fmp.csv', index=False)
    return data_df


if __name__ == '__main__':
    # Change this function call to save scrapped data to a csv file
    #scrape_tsx_from_advfn()
    data = scrape_fmp()
