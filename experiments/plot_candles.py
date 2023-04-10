import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


data = yf.download('TSLA',period='1y')
#print(data)

def plot_original(df):
    # https://levelup.gitconnected.com/creating-candlestick-plots-for-stocks-50c35b1573aa
    plt.style.use('dark_background')
    df['indices'] = range(len(df))
    width  = 0.5   # width of real body
    width2 = 0.01  # width of shadow

    fig, ax = plt.subplots(figsize=(15,10))
    # find the rows that are bullish
    dfup = df[df.Close >= df.Open]
    # find the rows that are bearish
    dfdown = df[df.Close < df.Open]
    # plot the bullish candle stick
    ax.bar(dfup.indices, dfup.Close - dfup.Open, width, 
           bottom = dfup.Open, edgecolor='g', color='green')
    ax.bar(dfup.indices, dfup.High - dfup.Close, width2, 
           bottom = dfup.Close, edgecolor='g', color='green')
    ax.bar(dfup.indices, dfup.Low - dfup.Open, width2, 
           bottom = dfup.Open, edgecolor='g', color='green')
    # plot the bearish candle stick
    ax.bar(dfdown.indices, dfdown.Close - dfdown.Open, width, 
           bottom = dfdown.Open, edgecolor='r', color='red')
    ax.bar(dfdown.indices, dfdown.High - dfdown.Open, width2, 
           bottom = dfdown.Open, edgecolor='r', color='red')
    ax.bar(dfdown.indices, dfdown.Low - dfdown.Close, width2, 
           bottom = dfdown.Close, edgecolor='r', color='red')
    ax.grid(color='lightgray')

    # set the ticks on the x-axis
    xtick_gap = 10
    ax.set_xticks(df[::xtick_gap]['indices'])
    # display the date for each x-tick
    _ = ax.set_xticklabels(labels = 
            df[::xtick_gap].index.strftime('%Y-%b-%d'), 
            rotation=45, ha='right')

    plt.show()

def plot_raw_from_bob(df):
    plt.style.use('dark_background')
    # Add Metadata for plotting ease
    df['indices'] = range(len(df))
    df['color'] = np.where(df.Close >= df.Open, 'green', 'red')
    df['CandleBase'] = np.where(df.Close >= df.Open, df.Open, df.Close)
    width_candle  = 0.5   # width of real body
    width_wick = 0.01  # width of shadow

    fig, ax = plt.subplots(figsize=(15,10))
    # Draw the wick (from low to high)
    ax.bar(df.indices, df.High - df.Low, width_wick, bottom = df.Low, edgecolor=df.color, color=df.color)
    # Draw the body
    ax.bar(df.indices, abs(df.Close - df.Open), width_candle, bottom=df.CandleBase, edgecolor=df.color, color=df.color)
    
    ax.grid(color='lightgray')

    # set the ticks on the x-axis
    xtick_gap = 10
    ax.set_xticks(df[::xtick_gap]['indices'])
    # display the date for each x-tick
    _ = ax.set_xticklabels(labels = 
            df[::xtick_gap].index.strftime('%Y-%b-%d'), 
            rotation=45, ha='right')

    plt.show()    

    return



#plot_raw_from_bob(data)
plot_raw_from_bob(data)