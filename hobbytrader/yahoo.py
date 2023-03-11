import pandas as pd
import yfinance as yf

from datetime import datetime, date


def yahoo_prices(tickers, current_day):
    # Return a DataFrame with dates, symbols and prices
    if not isinstance(tickers,list):
        return None
    if len(tickers) <= 1:
        return None

    years_back = 5
    end_dt = datetime.strptime(current_day, '%Y-%m-%d').date()
    start_dt = date(end_dt.year - years_back, end_dt.month, end_dt.day)

    data = yf.download(tickers, start=start_dt, end=end_dt)
    data = data.loc[(slice(None)),(slice(None),slice(None))].copy()
    data = data.stack()
    data = data.reset_index()
    data.rename(columns={'level_1': 'Symbol'}, inplace=True)
    data.set_index('Date', inplace=True)
    return data

def yahoo_minute_prices(tickers):
    if not isinstance(tickers,list):
        return None
    if len(tickers) <= 1:
        return None
    
    data = yf.download(tickers, period='1d', interval="1m", ignore_tz = True, prepost=False)
    
    data = data.loc[(slice(None)),(slice(None),slice(None))].copy()
    data = data.stack()
    data = data.reset_index()
    data.rename(columns={'level_1': 'Symbol'}, inplace=True)
    data.rename(columns={'level_0': 'Datetime'}, inplace=True)
    data.set_index('Datetime', inplace=True)
    return data

