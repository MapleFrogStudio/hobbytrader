import pandas as pd
import pandas_ta as ta
from hobbytrader import database

DB_PATH = 'DB/minute.sqlite'

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

def enter_trade(data, timeval):
    data.at[timeval, 'In_Position'] = True
    in_trade_length = 0

    return {'candles_in_trade': in_trade_length}




if __name__ == '__main__':
    data = database.load_OHLCV_from_db_for_symbols(DB_PATH, ['TSLA'])
    data = cast_column_types(data)
    data['EMA5'] = ta.ema(data.Close, 5)
    data['EMA200'] = ta.ema(data.Close, 200)
    data['EMAShortAboveLong'] = 0 # Moving Average Crossover
    data.loc[data['EMA5'] > data['EMA200'], 'EMAShortAboveLong'] = 1

    
    # TRADE ENTRY SIGNALS
    data['Long_Signal'] = None
    data['Trade_Entry'] = None
    data['Trade_BuyPrice'] = None
    data['Trade_TakeProfit'] = None
    data['Trade_StopLoss'] = None
    
    data['Long_Signal'] = (data['EMAShortAboveLong'] == 1) & (data['EMAShortAboveLong'].shift(1) == 0) # Only when the cross happens (Golden Cross)
    data.loc[(data['Long_Signal'].shift(1) == True), 'Trade_Entry'] = True
    data.loc[data["Trade_Entry"] == True, "Trade_BuyPrice"] = data['Open']
    data.loc[data["Trade_Entry"] == True, 'Trade_TakeProfit'] = data['Trade_BuyPrice'] * 1.05    # 5% higher sell for profit
    data.loc[data["Trade_Entry"] == True, 'Trade_StopLoss'] = data['Trade_BuyPrice'] * 0.98      # 2% lower sell for loss
    
    # TRADE MANAGEMENT COLUMNS
    data['In_Position'] = False    
    data['Sell_Signal'] = False
    data['Sell_Price'] = None
    data['Sell_Type'] = None

    # IMPLEMENT TRADE SIMULATION for Analysis    
    start_trade = 0
    end_trade_max = 20
    for timeval, row in data.iterrows():
        # if row['Enter_Trade']:
        #     in_trade_length = enter_trade(data, timeval) # Updates our DataFrame
        
        if row['Trade_Entry'] and not row['In_Position'] and start_trade < end_trade_max:
            data.at[timeval, 'In_Position'] = True
            start_trade += 1
            buy_price = row['Trade_BuyPrice']
            take_profit = row['Trade_TakeProfit']
            stop_loss = row['Trade_StopLoss']
        
        index_loc = data.index.get_loc(timeval)
        if  index_loc > 0:
            # If we are in our trade and did not reach max holding time, analyse exit conditions
            if data.iloc[index_loc - 1]['In_Position'] == True and start_trade < end_trade_max:
                start_trade += 1
                data.at[timeval, 'In_Position'] = True
                # TODO: Evaluate exit conditions
            else:
                if data.iloc[index_loc - 1]['In_Position'] == True and start_trade >= end_trade_max:
                    # Close position trigger
                    start_trade = 0
                    buy_price = None
                    take_profit = None
                    stop_loss = None
                    data.at[timeval, 'Sell_Signal'] = True

        

    data[-500:].to_csv('trades.csv', mode='w', header=True)        
    # Print out our results
    #for i in range(len(data)):
    #    row_printer(data.iloc[i], i)
        # if i > 10:
        #     break

    #print(data.loc[(data.Buy_Signal == 1) | (data.Enter_Trade == True)])
    #print(data.info())
