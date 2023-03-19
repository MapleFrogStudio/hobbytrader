import pandas as pd
import requests
import numpy as np
import io
import requests
# Import the correct module for symbols use
from hobbytrader import symbols

# Download a pandas DataFrame with the wikipedia table containing 
# all stock data included in the S&P 500 index
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
