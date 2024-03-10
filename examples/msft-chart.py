# https://youtu.be/TlhDI3PforA?si=5JxiPvrXL4NGNzl9&t=732
# Part Time Larry's demo and explanation of this code

import pandas as pd
import pandas_ta as ta
import yfinance as yf
from lightweight_charts import Chart

if __name__ == '__main__':
    chart = Chart()
    
    msft = yf.Ticker("MSFT")
    df = msft.history(period="1y")

    # prepare indicator values
    sma = df.ta.sma(length=20).to_frame()
    sma = sma.reset_index()
    sma = sma.rename(columns={"Date": "time", "SMA_20": "value"})
    sma = sma.dropna()

    # this library expects lowercase columns for date, open, high, low, close, volume
    df = df.reset_index()
    df.columns = df.columns.str.lower()
    chart.set(df)

    # add sma line
    line = chart.create_line()    
    line.set(sma)

    chart.watermark('MSFT')
    chart.show(block=True)