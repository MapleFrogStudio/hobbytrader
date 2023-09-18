import os
import json
import pandas as pd
import numpy as np

from hobbytrader import database

class TradeUniverse():
    TU_DATA_LOADED_FAIL = 0
    TU_DATA_LOADED_SUCCESS = 1
    TU_DATA_LOADED_PARTIAL = 2

    def __init__(self, symbols, load_data=True, db_path='DB/minute.sqlite'):
        self.symbols_requested = []
        self._valid_symbols = None
        # Sanity checks on constructor parameters
        if not isinstance(symbols, list):
            self.symbols_requested.append(symbols)
        if not all(map(lambda s: isinstance(s, str), symbols)):
            raise ValueError(f'{self.__class__}: Constructor only accepts list of strings')

        if not isinstance(load_data, bool):
            raise ValueError(f'{self.__class__}: Constructor load_data flag must be boolean')
        if not isinstance(db_path, str):
            raise ValueError(f'{self.__class__}: Constructor db_path must be a string')

        self.db_path = db_path
        self.reset_universe_meta_data()

        # If sanity checks passed, then symbols is a list of strings
        if len(self.symbols_requested) == 0:
            self.symbols_requested += symbols

        if load_data and self.found_in_db > 0:
            self.load_universe_data()
            self.update_universe_meta_data()

    def __json__(self):
        '''Return a python dictionary of relevant class attributes'''
        if self.datas is None:
            return None
        json_dict = {
            "DatasRows": len(self.datas),
            "DatesRange": {"First": self.dt_min, "Last":self.dt_max},
            "Dates": self.dates,
            "SymbolsRequested": self.symbols_requested,
            "SymbolsLoaded": self.loaded_symbols,
            "SymbolsNumber": len(self.loaded_symbols)
        }
        return json_dict

    @property
    def load_status(self) -> bool:
        if self.datas is None:
            return TradeUniverse.TU_DATA_LOADED_FAIL    
       
        if self.datas is not None:
            self.symbols_requested.sort()
            if self.loaded_symbols == self.symbols_requested:
                return TradeUniverse.TU_DATA_LOADED_SUCCESS
            else:
                return TradeUniverse.TU_DATA_LOADED_PARTIAL

    @property
    def found_in_db(self) -> int:
        symbols_list = self.symbols_requested
        if len(symbols_list) == 0:
            self._valid_symbols = None
            return 0
        
        valid_symbols = database.return_valid_symbols_from_list(symbols_list)
        if len(valid_symbols) > 0:
            self._valid_symbols = valid_symbols
            return len(valid_symbols)
        else:
            self._valid_symbols = None
            return 0

    @property
    def loaded_symbols(self) -> list:
        if self.datas is None:
            return None
        symbols = self.datas.Symbol.unique().tolist()
        symbols.sort()
        return symbols

    @property
    def dt_min(self):
        if self.datas is None:
            return None
        return self.dates.min()

    @property
    def dt_max(self):
        if self.datas is None:
            return None        
        return self.dates.max()

    @property
    def date(self):
        return self.dt_current

    @property
    def date_index(self):
        if self.date is None:
            return None
        return np.where(self.dates == self.date)[0][0]

    @date_index.setter
    def date_index(self, value):
        if value < 0:
            value = 0
        if value >= len(self.dates):
            value = len(self.dates) - 1
        self.dt_current = self.dates[value]

    def load_universe_data(self):
        '''Load Universe Data and update all meta_data
        '''
        if self._valid_symbols is None:
            self.datas = None
            self.reset_universe_meta_data()
            return
        if len(self._valid_symbols) == 0:
            self.datas = None
            self.reset_universe_meta_data()
            return
        
        self.datas = database.load_OHLCV_from_db_for_symbols(self.db_path, self._valid_symbols)
        self.datas = database.optimize_column_types(self.datas)        
        if len(self.datas) == 0:
            self.datas = None

    def reset_universe_meta_data(self) -> None:
        self.datas = None
        self.dates = None
        self.dt_current = None
    
    def update_universe_meta_data(self):
        self.dates = np.unique(self.datas.Datetime.values)
        self.dt_current = self.dates[0]

    def prices_for_date(self, dt=None):
        if dt is None:
            return None
        return self.datas.query("Datetime == @dt")
    
    def prices_for_dates(self, dt_start=None, dt_end=None):
        if dt_start is None or dt_end is None:
            return None
        if dt_end <= dt_start:
            return None

        return self.datas.query('@dt_start <= Datetime <= @dt_end')

    def symbol_by_id(self, id:int):
        if not isinstance(id, int):
            return None
        if id not in range(0,len(self.loaded_symbols)):
            return None
        
        return self.loaded_symbols[id]

    def id_by_symbol(self, symbol:str):
        if not isinstance(symbol, str):
            return None
        if symbol not in self.loaded_symbols:
            return None
        
        id = self.loaded_symbols.index(symbol)
        return id  

    def next_dt(self):
        dt_index = self.date_index
        if dt_index == len(self.dates):
            return False
        self.dt_current = self.dates[dt_index + 1]
        return True
    
    def prev_dt(self):
        dt_index = self.date_index
        if dt_index <= 0:
            return False
        self.dt_current = self.dates[dt_index - 1]
        return True
