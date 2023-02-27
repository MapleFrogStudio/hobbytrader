import datetime
import pandas as pd


from .symbols import grab_SP500_from_github_mfs_dataset as tickers
from .symbols import grab_tsx_stocks as tsx_tickers
from .yahoo import yahoo_minute_prices as minute_prices

def sp500():
    tickers_list = tickers().Yahoo.to_list()
    prices_df = minute_prices(tickers_list)
    date_obj = datetime.datetime.now()
    prices_df.to_parquet(f'DATASET/PARQUET/SP500-{date_obj.date()}.parquet', engine='pyarrow', index=True)
    prices_df.to_csv(f'DATASET/CSV/SP500-{date_obj.date()}.csv', index=True)

def tsx():
    tickers_list = tsx_tickers().YahooTicker.to_list()
    prices_df = minute_prices(tickers_list)
    date_obj = datetime.datetime.now()
    prices_df.to_parquet(f'DATASET/PARQUET/TSX-{date_obj.date()}.parquet', engine='pyarrow', index=True)
    prices_df.to_csv(f'DATASET/CSV/TSX-{date_obj.date()}.csv', index=True)
    