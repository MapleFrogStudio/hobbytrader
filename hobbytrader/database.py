# TODO :refactor this script in an OOP manner

import os
import pandas as pd
import sqlite3

from hobbytrader import DB_SQL_LIMIT
from hobbytrader.github import Github

def open_sqlite_db(db_file):
    conn = None
    conn = sqlite3.connect(db_file)
    #print(f'Sqlite version: {sqlite3.sqlite_version}')
    cursor = conn.cursor() 
    return conn, cursor   

def load_csv_prices_from_github(file_links):
    if not isinstance(file_links, list):
        return None
    
    merged_df = None
    print(f'\n')
    for file_url in file_links:
        print(f'Full path: {file_url}')
        loaded = pd.read_csv(file_url)
        loaded = loaded[['Datetime','Symbol','Open','High','Low','Close','Adj Close','Volume']]
        merged_df = pd.concat([merged_df, loaded])

    return merged_df

def generate_ID(prices_df):    
    print('Generating ID for each row [DATE + SYMBOL]')
    prices_df['ID'] = prices_df.Datetime.str.replace(" ", "")
    prices_df['ID'] = prices_df.ID.str.replace("-", "")
    prices_df['ID'] = prices_df.ID.str.replace(":", "")
    prices_df['ID'] = prices_df.ID + prices_df.Symbol
    return prices_df

def create_db_and_table(db_file) -> sqlite3.Connection:
    # Special function to create a database with a primary key that will ignore insert of an existing key
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
        #conn = sqlite3.connect(db_file)
        #print(f'Sqlite version: {sqlite3.sqlite_version}')
        #cursor = conn.cursor()
        conn, cursor = open_sqlite_db(db_file)
        cursor.execute(sql_create_prices_table)

    except sqlite3.Error as e:
        print(f'SQlite3 Error: {e}')
    
    return conn

#
# Save to specific file formats
# 
def save_to_sqlite(db_name, data_df):
    db_connection = create_db_and_table(db_name)
    if db_connection is None:
        print('No db connection established')
        return None
    data_df = generate_ID(data_df)    

    print('Indexing Dataframe on ID, converting Date strings to python Date Objects, this may take a while...')
    data_df = data_df.set_index('ID')
    data_df.Datetime = pd.to_datetime(data_df.Datetime)
    data_df = data_df[['Datetime','Symbol','Close','High','Low','Open','Volume']] # Get rid of 'Adj Close'
    data_df.to_sql('prices', db_connection, if_exists='append', index=True, index_label='ID')
    
    db_connection.close()

def save_to_csv(csv_name, data_df):
    data_df = generate_ID(data_df)
    print('Extracating unique IDs from merged prices....')
    data_df = data_df.drop_duplicates(subset=['ID'])
    data_df.to_csv(csv_name, index=False)

def save_to_parquet(file_name, data_df):
    data_df = generate_ID(data_df)
    print('Extracting unique IDs from merged prices....')
    data_df = data_df.drop_duplicates(subset=['ID'])
    data_df = data_df.drop(columns=['ID'])
    data_df = data_df.set_index('Datetime', drop=True)
    data_df.to_parquet(file_name, engine='pyarrow', index=True)

def load_OHLCV_from_db_for_symbols(db, symbols):
    ''' Return OHCLV price data for a list of symbols '''
    
    if not os.path.isfile(db):
        return None
    if not isinstance(symbols, list):
        return None

    db_conn, _ = open_sqlite_db(db)
    symbols_str = str(symbols)[1:-1]
    #sql_str = f"SELECT * FROM prices WHERE Symbol in ({symbols_str}) ORDER BY Datetime, Symbol"
    sql_str = f"SELECT * FROM prices WHERE Symbol in ({symbols_str}) "
    if DB_SQL_LIMIT > 0:
        sql_str += f' LIMIT {DB_SQL_LIMIT}'

    prices_df = pd.read_sql(sql_str, db_conn)
    prices_df = prices_df[['Datetime','Symbol','Open','High','Low','Close','Volume']]

    return prices_df

def optimize_column_types(df):
    '''Cast each column to smaller types for memory optimization '''
    df.Datetime = pd.to_datetime(df.Datetime)
    df.Symbol = df.Symbol.astype('category')
    df.Open = df.Open.astype('float32')
    df.High = df.High.astype('float32')
    df.Low = df.Low.astype('float32')
    df.Close = df.Close.astype('float32')
    df.Volume = df.Volume.astype('int')


    df = df.reset_index(drop=True)
    #df = df.set_index('Datetime')

    return df

def return_valid_symbols_from_list(symbols_list):
    db = 'DB/minute.sqlite'
    if not os.path.isfile(db):
        return None
    if not isinstance(symbols_list, list):
        return None
    db_conn, db_cursor = open_sqlite_db(db)

    sql_placeholder = ', '.join(['?'] * len(symbols_list))
    query = f"SELECT DISTINCT symbol FROM prices WHERE symbol IN ({sql_placeholder})"
    db_cursor.execute(query, symbols_list)
    existing_symbols = [row[0] for row in db_cursor.fetchall()]
    
    db_cursor.close()
    db_conn.close()

    return existing_symbols

    