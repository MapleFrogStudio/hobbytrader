import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import sys
import os
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta
import pandas as pd
from questdb.ingress import Sender, IngressError

from hobbytrader.github import Github

def get_urls_to_download(repo='DATASETS', subfolder='/DAILY', starts_with='SP500-2023-11'):
    owner = 'MapleFrogStudio'
    github_object = Github(repository=repo)
    files_to_load = github_object.file_links(folder=subfolder, starts_with=starts_with)
    
    return files_to_load

def fix_columns(data_df):
    if not 'Symbol' in data_df.columns:
        data_df = data_df.rename(columns={"Ticker": "Symbol"})

    return data_df

def load_data(url):
    #url ="https://raw.githubusercontent.com/MapleFrogStudio/DATA-2023-12/main/NASDAQ-BM0-2023-12-01.csv"
    data_df = pd.read_csv(url)

    data_df = fix_columns(data_df)

    data_df['Datetime'] = pd.to_datetime(data_df['Datetime'])
    data_df['Open'] = data_df['Open'].astype(float).round(2)
    data_df['High'] = data_df['High'].astype(float).round(2)
    data_df['Low'] = data_df['Low'].astype(float).round(2)
    data_df['Close'] = data_df['Close'].astype(float).round(2)
    data_df['Volume'] = data_df['Volume'].astype(int)

    #print(data_df)
    #print(f'Unique symbols: {data_df.Symbol.unique()}')
    print(f'Number of symbols: {len(data_df.Symbol.unique())}')
    
    return data_df

def send_data(data_df):
    host = os.getenv('QUESTDB_HOST')
    port = os.getenv("QUESTDB_PORT")
    db = os.getenv("QUESTDB_DB")

    print(f'Host: {host}, Port:{port}, DB:{db}')

    try:
        with Sender(host, port) as sender:
            sender.dataframe(
                data_df,
                table_name=db,  # Table name to insert into.
                symbols=['Symbol'],  # Columns to be inserted as SYMBOL types.
                at='Datetime')  # Column containing the designated timestamps.

    except IngressError as e:
        print(f'Got error: {e}\n')


def go(repo = 'DATA-2023-03', subfolder = '/', starts_with = 'NASDAQ-'):
    files_to_load = get_urls_to_download(
                        repo = repo, 
                        subfolder = subfolder, 
                        starts_with = starts_with
                    )

    #print(f'Repo:{repo}, Subfolder:{subfolder}, StartsWith:{starts_with}')
    #print(len(files_to_load))
    
    for file_url in files_to_load:
        print(file_url)
        data_df = load_data(file_url)
        print(f'Number of rows: {len(data_df)}')
        start_time = datetime.now()
        send_data(data_df)
        end_time = datetime.now()
        time_difference = end_time - start_time
        print(f'Data written to DB in {time_difference.total_seconds() / 60} minutes')

    print('END PROGRAM: Go')

if __name__ == '__main__':
    go(repo = 'DATA-2024-02', subfolder = '/', starts_with = 'tsx')
    # files_to_load = get_urls_to_download()
    # print(files_to_load)
    # data_df = load_data(files_to_load[10])
    # print(data_df)
    # send_data(data_df)


# QuestDB table creation must be created before running this script
# Officiel website for questdb: https://questdb.io/
        
# CREATE TABLE 'prices' (
#   Symbol SYMBOL capacity 256 CACHE,
#   Close DOUBLE,
#   High DOUBLE,
#   Low DOUBLE,
#   Open DOUBLE,
#   Volume LONG,
#   timestamp TIMESTAMP
# ) timestamp (timestamp) PARTITION BY DAY WAL
# DEDUP UPSERT KEYS(timestamp, Symbol);