import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, time
from dateutil.parser import parse

from hobbytrader import database

class TradeUniverse():
    def __init__(self, symbols:list, db_path='DB/minute.sqlite'):
        self.symbols_requested = []
        self.datas = None
        self.dates = None
        self.dt_current = None
        
        # Sanity checks on constructor parameters
        if not isinstance(symbols, list):
            raise ValueError(f'{self.__class__}: Constructor only accepts list of strings as symbols')                    
        if not all(map(lambda s: isinstance(s, str), symbols)):
            raise ValueError(f'{self.__class__}: Constructor only accepts list of strings as symbols')        
        
        if not isinstance(db_path, str):
            raise ValueError(f'{self.__class__}: Constructor db_path must be a string')
        if not os.path.isfile(db_path):
            raise ValueError(f'{self.__class__}: DB file "{db_path}" does not exist.')

        self.db_path = db_path
        self.db_first_date = database.min_date_in_db(self.db_path)
        self.db_last_date = database.max_date_in_db(self.db_path)
        self.db_total_rows = None # First call will fetch the count(*)
        
        self.symbols_requested = symbols
        if self.found_in_db == 0:
            raise ValueError(f'{self.__class__}: No symbols found in DB, will not be able to load data...')        

    def load_universe_data_all_dates(self):
        '''Load Universe Data with requested_symbols for all available dates'''
        self.datas = database.load_OHLCV_from_db_for_symbols(self.db_path, self._valid_symbols)
        self.datas = database.optimize_column_types(self.datas)        
        self.update_universe_meta_data()

    def load_universe_data_for_range(self, first_date, last_date):
        '''Load Universe Data with requested_symbols for date range (first and last date)'''
        # Sanity checks before launching an expensive database function
        try:
            start_dt = parse(first_date)
            end_dt = parse(last_date)
        except ValueError as e:
            raise ValueError(f'Invalid date passed as argument. {e}')

        if start_dt > end_dt:
            raise ValueError(f'Invalid dates passed as argument (last_date must be after first_date). {e}')

        # Make sure we grab the entire day if time is not specified
        if start_dt.time() == time(0, 0):
            start_dt = start_dt.replace(hour=0, minute=0, second=0)
        if end_dt.time() == time(0, 0, 0):
            end_dt = end_dt.replace(hour=23, minute=59, second=59)

        start_dt_str = start_dt.strftime('%Y-%m-%d %H:%M:%S')
        end_dt_str = end_dt.strftime('%Y-%m-%d %H:%M:%S')

        if self.found_in_db > 0:
            self.datas = database.load_OHLCV_from_db_for_dates(self.db_path, symbols=self.symbols_requested, dt_start=start_dt_str, dt_end=end_dt_str ) 
            self.datas = database.optimize_column_types(self.datas) 
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
    
    def __str__(self):
        return self.__json__()

    def to_json(self, indent=2):
        json_obj = self.__json__()
        if json_obj is None:
            return None
        return json.dumps(json_obj, indent = indent, default=str)     

    @property
    def load_status(self) -> bool:
        if self.datas is None:
            return False    
       
        if self.datas is not None:
            self.symbols_requested.sort()
            return True

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
        index = self.date_index
        if index >= len(self.dates)-1:
            return False
        self.dt_current = self.dates[index + 1]
        return True
    
    def prev_dt(self):
        dt_index = self.date_index
        if dt_index <= 0:
            return False
        self.dt_current = self.dates[dt_index - 1]
        return True

