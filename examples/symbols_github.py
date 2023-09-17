# Import the correct module for symbols use
from hobbytrader import symbols

def demo_sp500(symbols):
    symbols_df = symbols.grab_SP500_from_github_mfs_dataset()
    print(symbols_df.columns)

    print('--------------------------------')

    # Print all symbols with some company information available
    for index, row in symbols_df.iterrows():
        print(f'{index:3} Symbol:{row.Symbol.ljust(6)} Founded:{row.Founded[:4]}, Added: {str(row["Date added"]).ljust(10)}  Name: {row.Security}')

    print('--------------------------------')

    # Extract a list of symbols from the DataFrame and sort it alphabetically
    symbols = symbols_df.Symbol.to_list()
    symbols.sort()
    print(symbols)    

def demo_tsx(symbols):
    symbols_df = symbols.grab_tsx_stocks_from_github_mfs_dataset()
    print(symbols_df.columns)

    print('--------------------------------')

    # Print all symbols with some company information available
    for index, row in symbols_df.iterrows():
        print(f'{index:3} Symbol:{row.Symbol.ljust(6)} Name: {row.Name}')

    print('--------------------------------')

    # Extract a list of symbols from the DataFrame and sort it alphabetically
    symbols = symbols_df.Symbol.to_list()
    symbols.sort()
    print(symbols)    

def demo_nasdaq(symbols):
    # Pass one the Nasdaq sectors to the grab_nasdaq function
    sectors = ['', 'Consumer Defensive', 'Financial Services', 'Healthcare', 'Industrials', 'Technology', 'Consumer Cyclical', 'Basic Materials', 'Utilities', 'Communication Services', 'Real Estate', 'Energy']
    sector = sectors[1]
    symbols_df = symbols.grab_nasdaq_sector_from_github_mfs_dataset(sector=sector)
    print(symbols_df.columns)

    print('--------------------------------')

    # Print all symbols with some company information available
    for index, row in symbols_df.iterrows():
        print(f'{index:3} Symbol:{row.Symbol.ljust(6)} Name: {row.Name}')

    print('--------------------------------')

    # Extract a list of symbols from the DataFrame and sort it alphabetically
    symbols = symbols_df.Symbol.to_list()
    symbols.sort()
    print(symbols)    

if __name__ == '__main__':
    #demo_sp500(symbols)
    #demo_tsx(symbols)
    demo_nasdaq(symbols)
