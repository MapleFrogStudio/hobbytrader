# TODO :refactor this script in an OOP manner

import os
import pandas as pd
import sqlite3
from dateutil.parser import parse

from hobbytrader.github import Github

def open_sqlite_db(db_file):
    if not os.path.isfile(db_file):
        #return None
        raise ValueError(f'Database not found: {db_file}')
    
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

    if not isinstance(db_file, str):
        raise TypeError('Parameter not a string.')
    conn = None
    if not os.path.isfile(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor() 
        cursor.execute(sql_create_prices_table)
        return conn
    else:
        raise ValueError(f'Database already exists: {db_file}')
    
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
    
    if not isinstance(symbols, list):
        return None

    db_conn, _ = open_sqlite_db(db)  
    sql1 = f"SELECT * FROM prices WHERE Symbol IN ({', '.join(['?'] * len(symbols))}); "
    df1 = pd.read_sql_query(sql1, db_conn, params=symbols)

    df1 = df1[['Datetime','Symbol','Open','High','Low','Close','Volume']]
    return df1

def valid_date_format(dt):
    if dt is not None:
        try:
            parse(dt)
            return True
        except ValueError:
            raise ValueError("Invalid date format passed as parameter")  
    else:
        return False  

#TODO: Add load_OHCLV_from_db_for_dates.....
def load_OHLCV_from_db_for_dates(db, dt_start=None, dt_end=None):
    ''' Return OHCLV price data for a range of dates '''

    if not valid_date_format(dt_start):
        dt_start = min_date_in_db(db).strftime('%Y-%m-%d %H:%M:%S')
    if not valid_date_format(dt_end):
        dt_end = max_date_in_db(db).strftime('%Y-%m-%d %H:%M:%S')

    #dt_start = '2023-09-11 15:49:00'
    #dt_end = '2023-09-11 15:52:00'

    db_conn, _ = open_sqlite_db(db)  
    sql1 = f"SELECT * FROM prices WHERE Datetime >= :dt_start AND Datetime <= :dt_end;"
    df1 = pd.read_sql_query(sql1, db_conn, params={"dt_start":dt_start, "dt_end":dt_end})

    df1 = df1[['Datetime','Symbol','Open','High','Low','Close','Volume']]
    return df1


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

def max_date_in_db(db_file):
    conn, cursor = open_sqlite_db(db_file)
    sql_query = 'SELECT MAX(Datetime) FROM prices'
    cursor.execute(sql_query)
    max_date = [row[0] for row in cursor.fetchall()]
    return pd.to_datetime(max_date[0])

def min_date_in_db(db_file):
    conn, cursor = open_sqlite_db(db_file)
    sql_query = 'SELECT MIN(Datetime) FROM prices'
    cursor.execute(sql_query)
    min_date = [row[0] for row in cursor.fetchall()]
    return pd.to_datetime(min_date[0])


def generate_fake_data():
    ID =     ['20230428093000AAPL','20230428093100AAPL','20230428093200AAPL','20230428093300AAPL','20230428093400AAPL','20230428093500AAPL','20230428093600AAPL','20230428093700AAPL','20230428093000TSLA','20230428093100TSLA','20230428093200TSLA','20230428093300TSLA','20230428093400TSLA','20230428093500TSLA','20230428093600TSLA']
    Dates =  ['2023-04-28 09:30:00','2023-04-28 09:31:00','2023-04-28 09:32:00','2023-04-28 09:33:00','2023-04-28 09:34:00','2023-04-28 09:35:00','2023-04-28 09:36:00','2023-04-28 09:37:00','2023-04-28 09:30:00','2023-04-28 09:31:00','2023-04-28 09:32:00','2023-04-28 09:33:00','2023-04-28 09:34:00','2023-04-28 09:35:00','2023-04-28 09:36:00']
    Symbols= ['AAPL','AAPL','AAPL','AAPL','AAPL','AAPL','AAPL','AAPL','TSLA','TSLA','TSLA','TSLA','TSLA','TSLA','TSLA']
    Close =  [168.910995483398,168.720001220703,168.710098266602,168.365005493164,168.509994506836,168.225296020508,168.320007324219,168.369995117188,160.895004272461,160.119995117188,159.5,158.735000610352,158.426803588867,158.429992675781,158.679992675781]
    High =   [169.039993286133,168.960006713867,168.839996337891,168.710006713867,168.672607421875,168.550796508789,168.399993896484,168.399993896484,161.660003662109,161.039993286133,160.498901367188,159.539993286133,159.380004882813,158.979995727539,158.940002441406]
    Low =    [168.259994506836,168.679992675781,168.53010559082,168.339996337891,168.369995117188,168.220001220703,168.160003662109,168.229995727539,160.675506591797,160.110000610352,159.369995117188,158.668502807617,158.339996337891,158.220001220703,158.389999389648]
    Open =   [168.490005493164,168.910003662109,168.720001220703,168.710006713867,168.369995117188,168.505004882813,168.229995727539,168.320098876953,160.895004272461,160.895004272461,160.110000610352,159.539993286133,158.740005493164,158.401504516602,158.431503295898]
    Volume = [2030045.0, 268035.0, 261020.0, 210307.0, 213959.0, 183608.0, 235840.0, 189275.0,2863529.0, 701779.0, 689402.0, 730131.0, 790879.0, 563280.0, 442715.0]

    df = pd.DataFrame({
        'Datetime': Dates, 'Symbol': Symbols, 'Close': Close, 'High': High, 'Low': Low, 'Open': Open, 'Volume': Volume
    })
    return df.copy()    