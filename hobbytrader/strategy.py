import pandas as pd

from hobbytrader import symbols, yahoo

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

if __name__ == '__main__':
    
    # symbols_df = symbols.grab_nasdaq_sector_from_github_mfs_dataset('Real Estate')
    # symbols_df = symbols.grab_tsx_stocks_from_github_mfs_dataset()
    symbols_df = symbols.grab_SP500_from_github_mfs_dataset()
    symbols = symbols_df.Yahoo.to_list()
    #print(symbols)
    prices_df = yahoo.yahoo_prices(symbols, '2023-03-09')
    multi_asset = setup_multi_asset(prices_df)
    num_symbols = len(multi_asset)
    print(f'Number of symbols: {num_symbols}')
    for i in range(0,num_symbols):
        df = multi_asset[i]
        sym = df.iloc[0].Symbol
        #sym = 'Bidon'
        print(f'{i:03} : {sym: <10} contains {len(df):>4} price points')
