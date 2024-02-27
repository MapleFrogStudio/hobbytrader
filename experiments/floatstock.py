import sys
from numpy import isin
import yfinance as yf
from hobbytrader.github import grab_SP500_from_github_mfs_dataset as SP500
from hobbytrader.github import grab_tsx_stocks_from_github_mfs_dataset as TSX

tsx_df = TSX()
tsxyahoo = tsx_df.Yahoo.to_list()
#print(tsxyahoo)


sp500_df = SP500()
sp500yahoo = sp500_df.Yahoo.to_list()
# print(sp500yahoo)

#for symbol in tsxyahoo[0:50]:
for symbol in sp500yahoo[0:5]:
    # Define the ticker symbol for the stock you are interested in
    #ticker_symbol = 'SGMA'  # Example: Apple Inc.
    ticker_symbol = symbol

    # Create a Ticker object for the specified ticker symbol
    ticker = yf.Ticker(ticker_symbol)

    # Get the float and outstanding shares information
    try:
        info = ticker.info
        # Extract float and outstanding shares
        float_shares = info['floatShares']
        outstanding_shares = info['sharesOutstanding']
    except Exception as e:
        float_shares = 0
        outstanding_shares = 0


    print(f"{symbol} -> Float Shares:{float_shares}, {float_shares / 1000000:.0f}M")
    print(f"{symbol} -> Outstanding Shares: {outstanding_shares}, {outstanding_shares / 1000000:.0f}M")

