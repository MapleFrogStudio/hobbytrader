import os
import json
import pandas as pd

from hobbytrader import database

class TradeUniverse():
    TU_SYMBOLS_ALL_EXIST = 1
    TU_SYMBOLS_NONE_EXIST = 0
    TU_SYMBOLS_SOME_EXIST = 2
    TU_SYMBOLS_UNEXPECTED = -1

    TU_DATA_LOADED_FAIL = 0
    TU_DATA_LOADED_SUCCESS = 1

    def __init__(self, symbols, load_data=True, db_path='DB/minute.sqlite'):
        self.symbols_requested = []
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

        if load_data:
            self.load_status = self._check_for_symbols_in_db(symbols)
            self.load_universe_data()
            self.loaded = True

    def reset_universe_meta_data(self):
        self.datas = None
        self.load_status = None
        self.loaded = False
        self.valid_symbols = None
        self.dates = None
        self.dt_min = None
        self.dt_max = None
    
    def update_universe_meta_data(self):
        
        return True

    def _check_for_symbols_in_db(self, symbols_list):
        if len(symbols_list) == 0:
            return self.TU_SYMBOLS_UNEXPECTED
        
        valid_symbols = database.return_valid_symbols_from_list(symbols_list)
        valid_symbols.sort()
        symbols_list.sort()

        if len(valid_symbols) == 0:
            status = self.TU_SYMBOLS_NONE_EXIST
        elif valid_symbols == symbols_list:
            status = self.TU_SYMBOLS_ALL_EXIST
        elif len(valid_symbols) < len(symbols_list):
            status = self.TU_SYMBOLS_SOME_EXIST
        
        self.valid_symbols = valid_symbols
        return status
        
    def load_universe_data(self):
        '''Load Universe Data and update all meta_data
        '''
        if self.valid_symbols is None:
            return TradeUniverse.TU_DATA_LOADED_FAIL
        if len(self.valid_symbols) == 0:
            return TradeUniverse.TU_DATA_LOADED_FAIL
        
        self.datas = database.load_OHLCV_from_db_for_symbols(self.db_path, self.valid_symbols)
        
        if self.datas is None:
            return TradeUniverse.TU_DATA_LOADED_FAIL
        if len(self.datas) == 0:
            self.datas = None
            return TradeUniverse.TU_DATA_LOADED_FAIL

        success = self.update_universe_meta_data()
        if not success:
            return TradeUniverse.TU_DATA_LOADED_FAIL

        return TradeUniverse.TU_DATA_LOADED_SUCCESS
