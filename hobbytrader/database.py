import glob
import pandas as pd
import yfinance as yf
import sqlite3

from datetime import datetime, date, timedelta
from sqlite3 import Error

#
# Database generation section
#
def filenames_from_github_repo(base_name):
# TODO: Implement a function to list filenames from a github repo as a list
    filenames = glob.glob(f'DATASET\CSV\{base_name}*.csv')

    return filenames

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
        print(f'Sqlite version: {sqlite3.sqlite_version}')
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

    files_to_load = filenames_from_github_repo(base_name)

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
    build_sqlite_db_with_daily_minute_prices('sp500.sqlite3', 'SP500')
    build_sqlite_db_with_daily_minute_prices('nasdaq.sqlite3', 'NASDAQ')