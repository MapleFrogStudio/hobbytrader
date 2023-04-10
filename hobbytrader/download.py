import datetime
import pandas as pd


from .symbols import grab_SP500_from_github_mfs_dataset as sp500_tickers
from .symbols import grab_tsx_stocks_from_github_mfs_dataset as tsx_tickers
from .symbols import grab_nasdaq_sector_from_github_mfs_dataset as nasdaq_sector
from .yahoo import minute_prices as minute_prices

def sp500():
    tickers_list = sp500_tickers().Yahoo.to_list()
    prices_df = minute_prices(tickers_list)
    date_obj = datetime.datetime.now()
    prices_df.to_parquet(f'DATASET/PARQUET/SP500-{date_obj.date()}.parquet', engine='pyarrow', index=True)
    prices_df.to_csv(f'DATASET/CSV/SP500-{date_obj.date()}.csv', index=True)

def tsx():
    tickers_list = tsx_tickers().Yahoo.to_list()
    prices_df = minute_prices(tickers_list)
    date_obj = datetime.datetime.now()
    prices_df.to_parquet(f'DATASET/PARQUET/TSX-{date_obj.date()}.parquet', engine='pyarrow', index=True)
    prices_df.to_csv(f'DATASET/CSV/TSX-{date_obj.date()}.csv', index=True)

def nasdaq(tickers_list, sector_code):
    list_block_size = 800
    for i in range(0, len(tickers_list), list_block_size):
        #print(f'Index: {i}, Modulo:{i%(list_block_size-1)}')
        #print(tickers_list[i:i+list_block_size])
        subset_df = tickers_list[i:i+list_block_size].copy()
        prices_df = minute_prices(subset_df)
        
        blockid = i%(list_block_size-1)
        date_obj = datetime.datetime.now()
        prices_df.to_parquet(f'DATASET/PARQUET/NASDAQ-{sector_code}{blockid}-{date_obj.date()}.parquet', engine='pyarrow', index=True)
        prices_df.to_csv(f'DATASET/CSV/NASDAQ-{sector_code}{blockid}-{date_obj.date()}.csv', index=True)


def nasdaq_nosector():
    tickers = nasdaq_sector('')
    tickers_list = tickers.Yahoo.to_list()    
    nasdaq(tickers_list, 'NS')

def nasdaq_cd():
    tickers = nasdaq_sector('Consumer Defensive')
    tickers_list = tickers.Yahoo.to_list()    
    nasdaq(tickers_list, 'CD')

def nasdaq_fs():
    tickers = nasdaq_sector('Financial Services')
    tickers_list = tickers.Yahoo.to_list()    
    nasdaq(tickers_list, 'FS')

def nasdaq_healthcare():
    tickers = nasdaq_sector('Healthcare')
    tickers_list = tickers.Yahoo.to_list()    
    nasdaq(tickers_list, 'HC')

def nasdaq_industrials():
    tickers = nasdaq_sector('Industrials')
    tickers_list = tickers.Yahoo.to_list()    
    nasdaq(tickers_list, 'IN')

def nasdaq_technology():
    tickers = nasdaq_sector('Technology')
    tickers_list = tickers.Yahoo.to_list()    
    nasdaq(tickers_list, 'TE')

def nasdaq_cc():
    tickers = nasdaq_sector('Consumer Cyclical')
    tickers_list = tickers.Yahoo.to_list()    
    nasdaq(tickers_list, 'CC')

def nasdaq_bm():
    tickers = nasdaq_sector('Basic Materials')
    tickers_list = tickers.Yahoo.to_list()    
    nasdaq(tickers_list, 'BM')

def nasdaq_utilities():
    tickers = nasdaq_sector('Utilities')
    tickers_list = tickers.Yahoo.to_list()    
    nasdaq(tickers_list, 'UT')

def nasdaq_cs():
    tickers = nasdaq_sector('Communication Services')
    tickers_list = tickers.Yahoo.to_list()    
    nasdaq(tickers_list, 'CS')

def nasdaq_re():
    tickers = nasdaq_sector('Real Estate')
    tickers_list = tickers.Yahoo.to_list()    
    nasdaq(tickers_list, 'RE')

def nasdaq_energy():
    tickers = nasdaq_sector('Energy')
    tickers_list = tickers.Yahoo.to_list()    
    nasdaq(tickers_list, 'EN')

