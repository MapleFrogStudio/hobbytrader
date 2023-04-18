import re
import glob
import pandas as pd
import yfinance as yf
import sqlite3

import requests
from bs4 import BeautifulSoup

from datetime import datetime, date, timedelta
from sqlite3 import Error

GITHUB_URL = 'https://github.com/MapleFrogStudio/DATASETS/tree/main/DAILY'
GITHUB_RAW = 'https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/DAILY'

#
# Database generation section
#
def filenames_from_github_repo(base_name):
    github_url = GITHUB_URL
    result = requests.get(github_url)
    soup = BeautifulSoup(result.text, 'html.parser')
    #csvfiles = soup.find_all(title=re.compile(f"^{base_name}\.csv$"))
    csvfiles = soup.find_all(title=re.compile(f"^{base_name}."))

    file_names = [ ]
    for i in csvfiles:
        file_names.append(i.extract().get_text())
    print(file_names)    
    return(file_names)

def load_all_prices_from_github(filenames):
    merged_df = None
    for filename in filenames:
        file_to_load = f'{GITHUB_RAW}/{filename}'
        print(f'Full path: {file_to_load}')
        loaded = pd.read_csv(file_to_load)
        loaded = loaded[['Datetime','Symbol','Open','High','Low','Close','Adj Close','Volume']]
        #merged = pd.concat([merged,loaded]).drop_duplicates().reset_index(drop=True)
        merged_df = pd.concat([merged_df, loaded])
        
    return merged_df

def generate_ID(prices_df):    
    print('Generating ID for each row [DATE + SYMBOL]')
    prices_df['ID'] = prices_df.Datetime.str.replace(" ", "")
    prices_df['ID'] = prices_df.ID.str.replace("-", "")
    prices_df['ID'] = prices_df.ID.str.replace(":", "")
    prices_df['ID'] = prices_df.ID + prices_df.Symbol
    return prices_df

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

#
# Save to specific file formats
# 
def save_to_sqlite_db_with_daily_minute_prices(db_name, base_name):
    db_connection = _create_db_and_table(db_name)
    if db_connection is None:
        print('No db connection established')
        return None
    
    files_to_load = filenames_from_github_repo(base_name)
    prices_df = load_all_prices_from_github(files_to_load)
    prices_df = generate_ID(prices_df)
    
    print('Indexing Dataframe on ID, converting Date strings to python Date Objects, this may take a while...')
    prices_df = prices_df.set_index('ID')
    prices_df.Datetime = pd.to_datetime(prices_df.Datetime)
    prices_df = prices_df[['Datetime','Symbol','Close','High','Low','Open','Volume']] # Get rid of 'Adj Close'
    prices_df.to_sql('prices', db_connection, if_exists='append', index=True, index_label='ID')
    
    db_connection.close()

def save_to_csv_with_daily_minute_prices(csv_name, base_name):
    files_to_load = filenames_from_github_repo(base_name)
    prices_df = load_all_prices_from_github(files_to_load)
    prices_df = generate_ID(prices_df)
    print('Extrcating unique IDs from merged prices....')
    prices_df = prices_df.drop_duplicates(subset=['ID'])
    prices_df.to_csv(csv_name, index=False)

def save_to_parquet_with_daily_minute_prices(parquet_name, base_name):
    files_to_load = filenames_from_github_repo(base_name)
    prices_df = load_all_prices_from_github(files_to_load)
    prices_df = generate_ID(prices_df)
    print('Extrcating unique IDs from merged prices....')
    prices_df = prices_df.drop_duplicates(subset=['ID'])
    prices_df = prices_df.drop(columns=['ID'])
    prices_df = prices_df.set_index('Datetime', drop=True)
    prices_df.to_parquet(parquet_name, engine='pyarrow', index=True)


if __name__ == '__main__':
    #save_to_sqlite_db_with_daily_minute_prices('sp500.sqlite3', 'SP500')
    #save_to_slite_db_with_daily_minute_prices('TSX.sqlite3', 'TSX')
    #save_to_csv_with_daily_minute_prices('TSX.csv', 'TSX-2023-04')
    save_to_parquet_with_daily_minute_prices('TSX.parquet', 'TSX-2023-04')
    