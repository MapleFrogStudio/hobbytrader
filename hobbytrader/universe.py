import json
import pandas as pd
import pandas_ta as ta

class Indicators():
    def SMA(self, universe, period=50):
        SMA = pd.DataFrame()
        for asset in universe.symbols:
            df = universe.datas[universe.datas.Symbol == asset]
            asset_sma = ta.sma(df["Close"], length=period)
            # merge indicators for all assets to add a new column to universe datas
            SMA = pd.concat([SMA, asset_sma]) 

        return SMA        

    def EMA(self, universe, period=50):
        EMA = pd.DataFrame()
        for asset in universe.symbols:
            df = universe.datas[universe.datas.Symbol == asset]
            asset_ema = ta.ema(df["Close"], length=period)
            # merge indicators for all assets to add a new column to universe datas
            EMA = pd.concat([EMA, asset_ema]) 

        return EMA       


class TradeUniverse():
    def __init__(self, datas=None):
        self.symbols = None
        self.datas = pd.DataFrame()

        if not isinstance(datas, pd.core.frame.DataFrame):
            fake_df = self.generate_fake_data()
            self.add_datas(fake_df)
            #self.datas = self.generate_fake_data()
            self.fake_data = True
        else:
            if not self.valid_price_columns(datas):
                raise TypeError(f"Minimum columns required ['Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume'] found {[c for c in datas.columns]}")
            self.datas = datas
            self.fake_data = False

        self._update_universe()

    def add_datas(self, data_df):
        ''' Add Price DataFrame for multiple symbols '''
        if not self.valid_price_columns(data_df):
            raise TypeError(f"Minimum columns required ['Datetime', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume'] found {[c for c in data_df.columns]}")

        self.datas = pd.concat([self.datas, data_df], ignore_index=True)
        self._update_universe()


    def _update_universe(self):
        if self.symbols is None:
            self.symbols = []

        self.dates = self.datas.Datetime.values
        tmp_symbols = self.datas.Symbol.unique()
        new_symbols = [s for s in tmp_symbols if s not in self.symbols]
        self.symbols.extend(new_symbols) # Preserves existing order of dataset
        self.dt_min = self.dates.min()
        self.dt_max = self.dates.max()
        
    def indicators(self):
        self.I = Indicators()

    def __json__(self):
        '''Return a python dictionary'''
        dt_min = self.dt_min
        dt_max = self.dt_max
        json_dict = {
            'Records': len(self.datas),
            'NumberOfSymbols': len(self.symbols),
            'Symbols': self.symbols,
            'Dates': len(self.dates),
            'MinDate': dt_min,
            'MaxDate': dt_max
        }
        return json_dict

    def to_json(self, indent=2):
        json_obj = self.__json__()
        return json.dumps(json_obj, indent = indent, default=str) 
    
    def __str__(self):
        return f"{self.__json__()}"

    def valid_price_columns(self, data_df):
        if not isinstance(data_df, pd.DataFrame):
            return False
        if len(data_df.columns) < 7:
            return False
        if not 'Datetime' in data_df.columns or\
           not 'Symbol' in data_df.columns or\
           not 'Open' in data_df.columns or\
           not 'High' in data_df.columns or\
           not 'Low' in data_df.columns or\
           not 'Close' in data_df.columns or\
           not 'Volume' in data_df.columns:
            return False
        
        return True

    def symbol_by_id(self, id:int):
        if not isinstance(id, int):
            return None
        if id not in range(0,len(self.symbols)):
            return None
        
        return self.symbols[id]

    def id_by_symbol(self, symbol:str):
        if not isinstance(symbol, str):
            return None
        if symbol not in self.symbols:
            return None
        
        id = self.symbols.index(symbol)
        return id

    def generate_fake_data(self):
        ID =     ['20230428093000AAPL','20230428093100AAPL','20230428093200AAPL','20230428093300AAPL','20230428093400AAPL','20230428093500AAPL','20230428093600AAPL','20230428093700AAPL','20230428093000TSLA','20230428093100TSLA','20230428093200TSLA','20230428093300TSLA','20230428093400TSLA','20230428093500TSLA','20230428093600TSLA']
        Dates =  ['2023-04-28 09:30:00','2023-04-28 09:31:00','2023-04-28 09:32:00','2023-04-28 09:33:00','2023-04-28 09:34:00','2023-04-28 09:35:00','2023-04-28 09:36:00','2023-04-28 09:37:00','2023-04-28 09:30:00','2023-04-28 09:31:00','2023-04-28 09:32:00','2023-04-28 09:33:00','2023-04-28 09:34:00','2023-04-28 09:35:00','2023-04-28 09:36:00']
        Symbols= ['AAPL','AAPL','AAPL','AAPL','AAPL','AAPL','AAPL','AAPL','TSLA','TSLA','TSLA','TSLA','TSLA','TSLA','TSLA']
        Close =  [168.910995483398,168.720001220703,168.710098266602,168.365005493164,168.509994506836,168.225296020508,168.320007324219,168.369995117188,160.895004272461,160.119995117188,159.5,158.735000610352,158.426803588867,158.429992675781,158.679992675781]
        High =   [169.039993286133,168.960006713867,168.839996337891,168.710006713867,168.672607421875,168.550796508789,168.399993896484,168.399993896484,161.660003662109,161.039993286133,160.498901367188,159.539993286133,159.380004882813,158.979995727539,158.940002441406]
        Low =    [168.259994506836,168.679992675781,168.53010559082,168.339996337891,168.369995117188,168.220001220703,168.160003662109,168.229995727539,160.675506591797,160.110000610352,159.369995117188,158.668502807617,158.339996337891,158.220001220703,158.389999389648]
        Open =   [168.490005493164,168.910003662109,168.720001220703,168.710006713867,168.369995117188,168.505004882813,168.229995727539,168.320098876953,160.895004272461,160.895004272461,160.110000610352,159.539993286133,158.740005493164,158.401504516602,158.431503295898]
        Volume = [2030045.0, 268035.0, 261020.0, 210307.0, 213959.0, 183608.0, 235840.0, 189275.0,2863529.0, 701779.0, 689402.0, 730131.0, 790879.0, 563280.0, 442715.0]

        df = pd.DataFrame({
            'Datetime': Dates, 'Symbol': Symbols, 'Close': Close, 'High': High, 'Low': Low, 'Open': Open, 'Volume': Volume
        })
        return df.copy()

    def stats(self, symbols=None):
        if symbols == None:
            valid_symbols = self.symbols
        else:
            valid_symbols = [s for s in symbols if s in self.symbols]
        
        return valid_symbols
