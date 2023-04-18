# Financial Modeling Prep API Documentation
# https://site.financialmodelingprep.com/developer/docs/
import os
import json
import certifi
import pandas as pd

from urllib.request import urlopen
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('FMPAD_API_KEY')
print(api_key)


def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    data_df = pd.DataFrame(json.loads(data))
    return data_df

def get_tsx_tickers():
    exchange = 'TSX'
    sector = 'Technology'
    #url = f'https://financialmodelingprep.com/api/v3/stock-screener?sector={sector}&exchange={exchange}&apikey={api_key}'
    url = f'https://financialmodelingprep.com/api/v3/stock-screener?exchange={exchange}&apikey={api_key}'
    response = urlopen(url)
    data = response.read().decode("utf-8")
    data_df = pd.DataFrame(json.loads(data))
    return data_df


print('Program working...')

#symbol = 'AAPL'
#url = f'https://financialmodelingprep.com/api/v3/historical-chart/1min/{symbol}?apikey={api_key}'

#data = get_jsonparsed_data(url)
#print(f'{type(data)} --- {len(data)} rows)')
#print(data)

df1 = get_tsx_tickers()
#df1.to_csv('fmp-tsx.csv')
#filtered = df1.exchangeShortName == 'TSX'
#filtered = df1.isEtf == True
#filtered = df1.isActivelyTrading
#df1 = df1.loc[filtered].copy()
#df1 = df1[df1.symbol.str.contains(".TO")]
print(df1)

#df2 = pd.read_csv('https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO/tsx.csv')
#filtered = df2.Sector == 'Technology'
#df2 = df2.loc[filtered].copy()
#print(df2)

#df3 = pd.read_csv('https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO/tsxv.csv')
#filtered = df3.Sector == 'Technology'
#df3 = df3.loc[filtered].copy()
#print(df3)