import pandas as pd

def setup_multi_asset(prices_df):
    try:
        tickers = prices_df.Symbol.unique()
    except Exception as e:
        print(e)
    
    len_tickers = len(tickers)
    multi_assets = []
    for i in range(len_tickers):
        frame = prices_df.loc[prices_df.Symbol == tickers[i]].copy()
        multi_assets.append(frame)
    
    return multi_assets