import glob
import pandas as pd
import yfinance as yf
import sqlite3
import datetime

from datetime import datetime, date, timedelta
from sqlite3 import Error


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


#
# Database generation section
#
def _create_db_and_table(db_file) -> sqlite3.Connection:
    sql_create_prices_table = """ CREATE TABLE IF NOT EXISTS prices (
                                    ID text PRIMARY KEY ON CONFLICT IGNORE,
                                    Datetime timestamp NOT NULL,
                                    Symbol text NOT NULL,
                                    Close  real,
                                    High   real,
                                    Low    real,
                                    Open   real,
                                    Volume real
                                ); """    

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f'Sqlite version: {sqlite3.version}')
        cursor = conn.cursor()
        cursor.execute(sql_create_prices_table)

    except Error as e:
        print(e)
    
    return conn

def build_sqlite_db_with_daily_minute_prices(db_name, base_name):
    # create db connection
    # loop to read csv files with minute data
    # append data if non existant (what key? - date+stocksymbol)
    
    db_connection = _create_db_and_table(db_name)
    if db_connection is None:
        print('No db connection established')
        return

    files_to_load = glob.glob(f'DATASET\CSV\{base_name}*.csv')

    for file_name in files_to_load:
        print(file_name)
        prices_df = pd.read_csv(file_name)
        # create a unique key for databse insert
        prices_df['ID'] = prices_df.Datetime.str.replace(" ", "")
        prices_df['ID'] = prices_df.ID.str.replace("-", "")
        prices_df['ID'] = prices_df.ID.str.replace(":", "")
        prices_df['ID'] = prices_df.ID+prices_df.Symbol
        prices_df = prices_df.set_index('ID')
        prices_df.Datetime = pd.to_datetime(prices_df.Datetime)
        prices_df = prices_df[['Datetime','Symbol','Close','High','Low','Open','Volume']] # Get rid of 'Adj Close'
        prices_df.to_sql('prices', db_connection, if_exists='append', index=True, index_label='ID')

    db_connection.close()

if __name__ == '__main__':
    build_sqlite_db_with_daily_minute_prices('tsx.sqlite3', 'TSX')
    # build_sqlite_db_with_daily_minute_prices('sp500.sqlite3', 'SP500')
    # build_sqlite_db_with_daily_minute_prices('nasdaq.sqlite3', 'NASDAQ')