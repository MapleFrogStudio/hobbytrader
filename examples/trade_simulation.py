import pandas as pd
import pandas_ta as ta
from hobbytrader import database

DB_PATH = 'DB/minute.sqlite'
MAX_CANDLES_IN_TRADE = 390 * 5          # 390 candles = 1 day
SYMBOLS = ['TSLA']                      # Example only works for 1 symbol :(

def cast_column_types(df):
    df.Datetime = pd.to_datetime(df.Datetime)
    df.Symbol = df.Symbol.astype('category')
    df.Open = df.Open.astype('float32')
    df.High = df.High.astype('float32')
    df.Low = df.Low.astype('float32')
    df.Close = df.Close.astype('float32')
    df.Volume = df.Volume.astype('int')

    df = df.reset_index()
    df = df.set_index('Datetime')

    return df

def execute_buy_if_signaled(data, timeval, index_loc):
    '''
    If previous row In_Position is True, ignore the long_signal we have already bought the asset
    If previous row In_Position is False, Check id Long_Signal
    '''

    if index_loc < 1:
        return  # Always skip first candle

    if data.iloc[index_loc - 1]['InPosition']:    
        return  # Do nothing we are already in position

    if data.iloc[index_loc - 1]['LongSignal']:
        # Enter long trade
        data.at[timeval, 'InPosition']  = True
        data.at[timeval, 'TradeStatus'] = 'Enter'
        data.at[timeval, 'BuyPrice']    = data.loc[timeval, 'Open']
        data.at[timeval, 'TradeTarget'] = data.loc[timeval, 'BuyPrice'] * 1.05    # 5% higher sell for profit
        data.at[timeval, 'TradeStop']   = data.loc[timeval, 'BuyPrice'] * 0.98      # 2% lower sell for loss
        data.at[timeval, 'TradeMaxCandles'] = MAX_CANDLES_IN_TRADE
        data.at[timeval, 'CandlesInTrade'] = 1
    

def manage_in_position_flags(data, timeval, index_loc):
    if index_loc < 1:
        return  # Always skip first candle
    
    if data.iloc[index_loc-1]['InPosition'] and data.iloc[index_loc-1]['SellSignal'] != True:
        data.at[timeval, 'InPosition'] = True
        data.at[timeval, 'CandlesInTrade'] = data.iloc[index_loc - 1]['CandlesInTrade'] + 1
        data.at[timeval, 'BuyPrice'] = data.iloc[index_loc - 1]['BuyPrice']
        data.at[timeval, 'TradeTarget'] = data.iloc[index_loc - 1]['TradeTarget']
        data.at[timeval, 'TradeStop'] = data.iloc[index_loc - 1]['TradeStop']
        data.at[timeval, 'TradeMaxCandles'] = data.iloc[index_loc - 1]['TradeMaxCandles']
        
        

def update_exit_conditions(data, timeval, index_loc):
    if index_loc < 1:
        return  # Always skip first candle

    if data.loc[timeval]['InPosition']:
        candles_in_trade = data.loc[index_loc - 1]['CandlesInTrade']
        if int(data.loc[timeval]['CandlesInTrade']) > MAX_CANDLES_IN_TRADE:
            data.at[timeval, 'SellSignal'] = True
            data.at[timeval, 'SellType'] = 'Close'
            data.at[timeval, 'CandlesInTrade'] = 0
            data.at[timeval, 'InPositionCandles'] = candles_in_trade
        elif data.loc[timeval]['Close'] > data.loc[timeval]['TradeTarget']:
            data.at[timeval, 'SellSignal'] = True
            data.at[timeval, 'SellType'] = 'Target'
            data.at[timeval, 'CandlesInTrade'] = 0        
            data.at[timeval, 'InPositionCandles'] = candles_in_trade            
        elif data.loc[timeval]['Close'] < data.loc[timeval]['TradeStop']:
            data.at[timeval, 'SellSignal'] = True
            data.at[timeval, 'SellType'] = 'Stop'
            data.at[timeval, 'CandlesInTrade'] = 0  
            data.at[timeval, 'InPositionCandles'] = candles_in_trade            


def execute_sell_if_signaled(data, timeval, index_loc):
    if index_loc < 1:
        return  # Always skip first candle

    if data.loc[index_loc - 1]['SellSignal']:
        data.at[timeval, 'InPosition'] = False
        data.at[timeval, 'CandlesInTrade'] = 0
        data.at[timeval, 'SellPrice'] = data.loc[timeval]['Open']
        data.at[timeval, 'SellType'] = data.iloc[index_loc-1]['SellType']
        data.at[timeval, 'TradeStatus'] = 'Exit'
        data.at[timeval, 'InPositionCandles'] = data.iloc[index_loc-1]['InPositionCandles']

def analyze_trades(trades_file):
    raw_trades = pd.read_csv('trades.csv')
    TradeEntries = raw_trades[raw_trades['TradeStatus'] == 'Enter']
    TradeExits = raw_trades[raw_trades['TradeStatus'] == 'Exit']
    df1 = TradeEntries[['Datetime', 'Symbol', 'Open','High','Low','Close','Volume','TradeStatus','BuyPrice','TradeTarget','TradeStop','TradeMaxCandles']].copy()
    df1 = df1.reset_index()
    df2 = TradeExits[['Datetime','TradeStatus','CandlesInTrade','SellPrice','SellType','InPositionCandles']].copy()
    df2 = df2.reset_index()
    trades_df = pd.concat([df1, df2], axis=1)
    trades_df
    closes = trades_df[trades_df['SellType'] == 'Close']['SellType'].count()
    targets = trades_df[trades_df['SellType'] == 'Target']['SellType'].count()
    stops = trades_df[trades_df['SellType'] == 'Stop']['SellType'].count()
    return {'Closes':closes, 'Targets':targets, 'Stops':stops}
    #print(f'Closes:{closes}, Targets:{targets}, Stops:{stops}')


if __name__ == '__main__':
    # LOAD MINUTE DATA
    data = database.load_OHLCV_from_db_for_symbols(DB_PATH, ['TSLA'])
    #data = cast_column_types(data)

    # SETUP INDICATORS
    data['EMA5'] = ta.ema(data.Close, 5)
    data['EMA200'] = ta.ema(data.Close, 200)
    data['EMAShortAboveLong'] = 0 # Moving Average Crossover
    data.loc[data['EMA5'] > data['EMA200'], 'EMAShortAboveLong'] = 1

    # SETUP BUY LONG SIGNAL
    data['LongSignal'] = (data['EMAShortAboveLong'] == 1) & (data['EMAShortAboveLong'].shift(1) == 0)      # Only when the cross happens (Golden Cross)

    
    # TRADE ENTRY SIGNALS
    data['TradeStatus'] = None
    data['BuyPrice'] = None
    data['TradeTarget'] = None
    data['TradeStop'] = None
    data['TradeMaxCandles'] = None
    data['CandlesInTrade'] = 0
    # TRADE MANAGEMENT COLUMNS
    data['InPosition'] = False    
    data['SellSignal'] = None
    data['SellPrice'] = None
    data['SellType'] = None
    data['InPositionCandles'] = None

    # IMPLEMENT TRADE SIMULATION FOR ANALYSIS (Backtesting)    
    
    for timeval, _ in data.iterrows():
        index_loc = data.index.get_loc(timeval)
        execute_buy_if_signaled(data, timeval, index_loc)       # Check previous candle for buy signal and execute it
        manage_in_position_flags(data, timeval, index_loc)      # Check if a buy was executed and adjust inPosition flags (including price brackets)
        update_exit_conditions(data, timeval, index_loc)        # While in condition and no sell_signal, update exit conditions (Max_Trade_Lebgth, Target, Stop)
        execute_sell_if_signaled(data, timeval, index_loc)      # Check previous candle for sell signal and execute it

    # SAVE OUR DATA FOR ANALYSIS
    data.to_csv('trades.csv', mode='w', header=True, index=False)        

    # ANALYSE TRADES FOR PROFITABILITY
    performance = analyze_trades('trades.csv')
    print(performance)


