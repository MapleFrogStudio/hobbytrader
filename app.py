import json
import psutil

import plotly.graph_objects as go
import pandas as pd

from hobbytrader import database
#from hobbytrader.symbols import grab_tsx_stocks_from_github_mfs_dataset as tsx_symbols
from hobbytrader.universe import TradeUniverse
from hobbytrader import scrappers
from datetime import datetime

def print_mem(msg):
    memory_info = psutil.virtual_memory()   # Get system-wide memory usage
    total_memory = memory_info.total        # Total available memory
    used_memory = memory_info.used          # Memory used by all processes
    free_memory = memory_info.available     # Free memory available

    print(msg)
    print(f"Total Memory: {total_memory / (1024 ** 3):.2f} GB")
    print(f"Used Memory: {used_memory / (1024 ** 3):.2f} GB")
    print(f"Free Memory: {free_memory / (1024 ** 3):.2f} GB")  
    print(f'--------------------------------------------------------------------')

def scrapers():
    advfn = scrappers.ADVFN()
    df = advfn.scrape_data()
    print(df)
    advfn.to_csv()
    input('Press ENTER To continue')

    fmpad = scrappers.FMPAD()
    df = fmpad.scrape_data()
    print(df)
    fmpad.to_csv()
    input('Press ENTER To continue')

    wiki = scrappers.wikipedia_SP500()
    df = wiki.scrape_data()
    print(df)
    wiki.to_csv()
    print(wiki.history())    
    input('Press ENTER To continue')

def main():
    db_path = 'DB/minute.sqlite'
    symbols = ['TSLA', 'AAPL', 'GIB-A.TO']

    #tsx = tsx_symbols()
    #symbols = tsx.Yahoo.tolist()
    print_mem('Data loading please wait...')
    u = TradeUniverse(symbols, db_path=db_path)
    print_mem('Data loaded...')
    print(f'Symbols: {symbols}')
    print(f'Number of datas record: {len(u.datas)}')
    index = 2
    print(f"Check for {symbols[index]} presence\n {u.datas.query('Symbol == @symbols[@index]').head(5)}")
    print('-----')

    u.date_index = 1000
    while True:
        print(f'Current date: {u.date}')
        print(u.prices_for_date(u.date))
        user_input = input('ENTER - Next date, CTRL-C Quit')
        if not u.next_dt():
            break
        print_mem(f'Index loop {u.date_index}...')

def do_trades():
    symbols = ['TSLA', 'AAPL', 'GIB-A.TO']   
    u = TradeUniverse(symbols)
    u.load_universe_data_all_dates()
    print(f'Loaded symbols: {u.loaded_symbols}')
    print(f'DB first date: {u.db_first_date}, DB Last date: {u.db_last_date}')
    print(u.datas)

def plotly_demo():
    #https://plotly.com/python/candlestick-charts/
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                    open=df['AAPL.Open'],
                    high=df['AAPL.High'],
                    low=df['AAPL.Low'],
                    close=df['AAPL.Close'])])
    
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()

def plot():
    db_path = 'DB/minute.sqlite'
    symbols = ['TSLA', 'AAPL', 'GIB-A.TO']
    print_mem('Data loading please wait...')
    u = TradeUniverse(symbols, db_path=db_path)
    u.load_universe_data_all_dates()

    df = u.datas[u.datas.Symbol == 'TSLA'][-100:]
    fig = go.Figure(data=[go.Candlestick(x=df['Datetime'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])

    # fig.update_xaxes(
    #     rangeslider_visible=False,
    #     rangebreaks=[
    #         # NOTE: Below values are bound (not single values), ie. hide x to y
    #         dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
    #         dict(bounds=[16, 9.5], pattern="hour"),  # hide hours outside of 9.30am-4pm
    #         # dict(values=["2019-12-25", "2020-12-24"])  # hide holidays (Christmas and New Year's, etc)
    #     ]
    # )

    #fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()


if __name__ == '__main__':
    print_mem('Start of program')
    #scrapers()
    #do_trades()
    plot()
