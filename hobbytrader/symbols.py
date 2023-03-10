import pandas as pd
import requests
import numpy as np
import io
import requests
import re
import string
import time

from bs4 import BeautifulSoup


def grab_from_HTML_file():
    # Grab S&P Symbols from Wikipedia or local HTML File
    # wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    # wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks'
    tickers = pd.read_html("./tickers.html")[0]
    tickers_df = tickers[0]
    tickers_df['Yahoo'] = [s.replace('.', '-') for s in tickers_df.Symbol]

    return tickers_df


def grab_SP500_from_wikipedia():
    # wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks'
    wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    s = requests.get(wiki_url).content
    tickers = pd.read_html(io.StringIO(s.decode("utf-8")))
    tickers_df = tickers[0]
    tickers_df['Yahoo'] = [s.replace('.', '-') for s in tickers_df.Symbol]
    return tickers_df


def grab_SP500_from_github_mfs_dataset() -> pd.DataFrame:
    url = "https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/CSV/sp500.csv"
    tickers_df = pd.read_csv(url, header=0, index_col=None)
    tickers_df['Yahoo'] = [s.replace('.', '-') for s in tickers_df.Symbol]
    return tickers_df

def grab_tsx_stocks_from_github_mfs_dataset() -> pd.DataFrame:
    url = "https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO/tsx.csv"
    tickers_df = pd.read_csv(url, header=0, index_col=None, keep_default_na=False)
    tickers_df['Yahoo'] = [f"{s.replace('.', '-')}.TO" for s in tickers_df.Symbol]
    tickers_df = tickers_df.loc[tickers_df.Type == 'EQUITY']
    
    return tickers_df

def grab_nasdaq_sector_from_github_mfs_dataset(sector='Energy') -> pd.DataFrame:
    nasdaq_url = 'https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO/nasdaq.csv'
    nasdaq_df = pd.read_csv(nasdaq_url, header=0, index_col=None, keep_default_na=False)
    nasdaq_df.rename(columns={'YahooTicker':'Yahoo'}, inplace=True)
    sector_df = nasdaq_df.loc[nasdaq_df.Type == 'EQUITY'].copy()
    sector_df = sector_df.loc[sector_df.Sector == sector].copy()
    return sector_df

def scrap_advfn():
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }    
    url_base = 'https://ca.advfn.com/investing/stocks/canada/tsx?letter='
    letters = list(string.ascii_uppercase)
    letters.append('0')
    pattern = r'TSX\/(.*?)\/stock-price' # Extract symbol from url

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
            url = a_tag['href']
            ticker = re.findall(pattern, url)[0]
            symbol_info = {"Symbol":ticker, "Name":name, "Url":url}
            symbols_list.append(symbol_info)
            #print(f'{ticker: <10} : {name} -> {url}')
        time.sleep(1)

    symbols_df = pd.DataFrame(symbols_list)
    return symbols_df

    

if __name__ == '__main__':
    symbols_df = scrap_advfn()
    symbols_df.to_csv('test.csv')