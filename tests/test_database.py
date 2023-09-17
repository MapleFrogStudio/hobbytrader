import os
import time
import sqlite3 
import pandas as pd
import numpy as np
import pytest

from hobbytrader.github import Github
from hobbytrader import database

@pytest.fixture(scope="session")
def file_links():
    repo = 'DATASETS'
    filter = 'TSX-2023-06-17'
    github_object = Github(repository=repo)
    file_links_list = github_object.file_links(folder='DAILY', starts_with=filter)
    filter = 'TSX-2023-06-18'
    github_object = Github(repository=repo)
    file_links_duplicates = github_object.file_links(folder='DAILY', starts_with=filter)
    file_links_list.extend(file_links_duplicates)

    return file_links_list

@pytest.fixture(scope="session")
def load_price_data(file_links):
    csv_files = file_links
    data_df = database.load_csv_prices_from_github(csv_files)

    return data_df

def test_load_csv_prices_from_github(file_links):
    csv_files = file_links
    assert len(csv_files) > 0

    data = database.load_csv_prices_from_github(csv_files)
    assert data is not None

def test_load_csv_prices_from_github_bad_parameter():
    data = database.load_csv_prices_from_github('bad')
    assert data is None

def test_generate_ID(load_price_data):
    data = load_price_data.copy()
    data = database.generate_ID(data)  
    assert 'ID' in data.columns

def test_open_sqlite_db():
    db_file = 'tests/test.sqlite'
    conn, cursor = database.open_sqlite_db(db_file)
    assert conn is not None
    assert cursor is not None
    conn.close()
    if os.path.isfile(db_file):
        os.remove(db_file)
    assert not os.path.isfile(db_file)

def test_create_db_and_table_file_created():
    test_file = 'tests/test.sqlite'
    db_connection = database.create_db_and_table(test_file)
    assert db_connection is not None
    db_connection.close()
    if os.path.isfile(test_file):
        os.remove(test_file)
    assert not os.path.isfile(test_file)

def test_create_db_and_table_conflict_on_insert():
    test_file = 'tests/test.sqlite3'
    db_connection = database.create_db_and_table(test_file)

    # Try to insert the same data twice to check if create DB's PRIMARY KEY ON CONFLICT IGNORE works
    data = {
        'ID'      : ['20230217093000A'],
        'Datetime': ['2023-02-17 09:30:00'],
        'Symbol'  : ['A'],
        'Close'   : ['147.014999389648'], 
        'High'    : ['147.270004272461'],
        'Low'     : ['146.919998168945'], 
        'Open'    : ['147.259994506836'], 
        'Volume'  : ['39644.0'],
    }
    df = pd.DataFrame(data)
    df = df.set_index('ID')
    df.to_sql('prices', db_connection, if_exists='append', index=True, index_label='ID')               
    df.to_sql('prices', db_connection, if_exists='append', index=True, index_label='ID')               
    # Read thesaved data, should only have one line
    query = "SELECT * FROM prices"
    new_df = pd.read_sql_query(query, db_connection)
    assert len(new_df) == 1
    #Close and delete our test DB
    db_connection.close()
    if os.path.isfile(test_file):
        os.remove(test_file)

def test_create_db_and_table_type_error():
    with pytest.raises(TypeError):
        test_file = 10 # Make sur this is not a string
        db_connection = database.create_db_and_table(test_file)

def test_save_to_sqlite(load_price_data):
    db_name = 'tests/test.sqlite3'
    data_df = load_price_data.copy()
    database.save_to_sqlite(db_name, data_df)

    # Reload saved data for assert statement
    cnx = sqlite3.connect(db_name)
    reload_df = pd.read_sql_query("SELECT * FROM prices", cnx)
    cnx.close()

    # Drop duplicates from DF to compare with insert DB that does not duplicate
    count1 = data_df.drop_duplicates(subset=['Datetime','Symbol']).shape[0]
    count2 = reload_df.shape[0]
    assert count1 == count2
    
    # Remove saved test file
    if os.path.isfile(db_name):
        os.remove(db_name)

def test_save_to_sqlite_no_file(load_price_data):
    db_name = 'NOFOLDER/nofile.sqlite'
    data_df = load_price_data.copy()
    database.save_to_sqlite(db_name, data_df)    

def test_save_to_csv(load_price_data):
    file_name = 'test.csv'
    data_df = load_price_data.copy()
    database.save_to_csv(file_name, data_df)

    # Reload saved data for assert statement
    reload_df = pd.read_csv(file_name)

    count1 = data_df.drop_duplicates(subset=['Datetime','Symbol']).shape[0]
    count2 = reload_df.shape[0]
    assert count1 == count2
    
    # Remove saved test file
    if os.path.isfile(file_name):
        os.remove(file_name)     

def test_save_to_parquet(load_price_data):
    file_name = 'test.parquet'
    data_df = load_price_data.copy()
    count1 = data_df.drop_duplicates(subset=['Datetime','Symbol']).shape[0]

    database.save_to_parquet(file_name, data_df)

    # Reload saved data for assert statement
    reload_df = pd.read_parquet(file_name, engine='pyarrow')
    count2 = reload_df.shape[0]
    assert count1 == count2
    
    # Remove saved test file
    if os.path.isfile(file_name):
        os.remove(file_name)    

def test_load_OHLCV_from_db_for_symbols_noDBfile():
    dbpath = 'DB/nofile.sqlite'
    data = database.load_OHLCV_from_db_for_symbols(dbpath, ['TSLA'])
    assert data is None

def test_load_OHLCV_from_db_for_symbols_not_a_list():
    dbpath = 'DB/minute.sqlite'
    symbol = 'TSLA'
    data = database.load_OHLCV_from_db_for_symbols(dbpath, symbol)
    assert data is None

def test_load_OHLCV_from_db_for_symbols_return_df():
    dbpath = 'DB/minute.sqlite'
    symbols = ['TSLA', 'AAPL']
    data = database.load_OHLCV_from_db_for_symbols(dbpath, symbols)
    assert data is not None
    assert isinstance(data, pd.DataFrame)
    assert 'Symbol' in data.columns
    assert 'Open'   in data.columns
    assert 'High'   in data.columns
    assert 'Low'    in data.columns
    assert 'Close'  in data.columns
    assert 'Volume' in data.columns
    print(data)

def test_optimize_column_types():
    dbpath = 'DB/minute.sqlite'
    symbols = ['TSLA', 'AAPL']
    data = database.load_OHLCV_from_db_for_symbols(dbpath, symbols)
    data = database.optimize_column_types(data)
    assert data is not None
    assert isinstance(data.Datetime.values[0], np.datetime64)
    assert pd.api.types.is_categorical_dtype(data.Symbol)
    assert data.Open.dtype == np.float32
    assert data.High.dtype == np.float32
    assert data.Low.dtype == np.float32
    assert data.Close.dtype == np.float32
    assert data.Volume.dtype == np.int32

def test_return_valid_symbols_from_list():
    requested_symbols = ['AAPL','TSLA','BadSymbol','GIB-A.TO']
    valid_symbols = database.return_valid_symbols_from_list(requested_symbols)

    assert valid_symbols is not None
    assert len(valid_symbols) < len(requested_symbols)

def test_return_valid_symbols_from_list_bad_list():
    invalid_list = 'AAPL'
    valid_symbols = database.return_valid_symbols_from_list(invalid_list)
    assert valid_symbols is None

def test_return_valid_symbols_from_list_No_symbols_found():
    requested_symbols = ['NoGood1','NoGood2']
    valid_symbols = database.return_valid_symbols_from_list(requested_symbols)
    assert valid_symbols is not None
    assert len(valid_symbols) == 0