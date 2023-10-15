'''Test script for TradeUniverse. Assumes example/build_db was run and roduced a database called DB/minute.sqlite'''
import pytest
from hobbytrader import github
from hobbytrader.universe import TradeUniverse
import datetime

def test_TradeUniverse_constructor_with_good_symbols():
    symbols = ['AAPL','TSLA']
    u = TradeUniverse(symbols)
    assert u is not None
    assert u.datas is None
    assert u.load_status == False
    assert len(u.symbols_requested) == 2

def test_TradeUniverse_constructor_with_some_symbols():
    symbols = ['AAPL','TSLA', 'NoGood']
    u = TradeUniverse(symbols)
    assert u is not None
    assert u.datas is None
    assert u.load_status == False
    assert len(u.symbols_requested) == 3

# SERIES OF TESTS TO CHECK construtor errors
def test_TradeUniverse_constructor_with_all_bad_symbols():
    symbols = ['NoGood1','NoGood2']
    with pytest.raises(ValueError):
        u = TradeUniverse(symbols)

def test_TradeUniverse_constructor_no_parameters():
    with pytest.raises(TypeError):
        u = TradeUniverse()

def test_TradeUniverse_constructor_with_string():
    with pytest.raises(ValueError):
        u = TradeUniverse('TSLA')

@pytest.mark.parametrize("non_strings_list",[
    (['TSLA',1]), (1,'TSLA'), ('TSLA',True)
])
def test_TradeUniverse_constructor_non_string_in_list(non_strings_list):
    with pytest.raises(ValueError):
        u = TradeUniverse(non_strings_list)

def test_TradeUniverse_constructor_db_path_non_string():
    with pytest.raises(ValueError):
        u = TradeUniverse(['TSLA','AAPL'], db_path=10)

def test_TradeUniverse_constructor_db_path_not_found():
    with pytest.raises(ValueError):
        u = TradeUniverse(['TSLA','AAPL'], db_path='nodbfile.sqlite')


# TEST UNIVERSE with data loading and all stats
def test_load_universe_all_dates():
    symbols = ['AAPL','TSLA']
    u = TradeUniverse(symbols)
    u.load_universe_data_all_dates()

    assert u is not None
    assert u.symbols_requested == symbols
    assert u.loaded_symbols.sort() == symbols.sort()
    assert u.load_status == True
    assert u.datas is not None
    assert u.dates is not None
    assert len(u.dates) > 0

    print(f'\nsymbols_Requested: {len(u.symbols_requested)}, Dates loaded: {len(u.dates)}, Symbols_loaded: {len(u.loaded_symbols)}')

# RENDU ICI POUR CORRGER Load for date ainsi que les tests assoicés

def test_load_universe_for_range():
    #tsx = github.grab_tsx_stocks_from_github_mfs_dataset()
    #symbols = tsx.Yahoo.to_list()
    symbols = ['TSLA','AAPL','GIB-A.TO']
    u = TradeUniverse(symbols=symbols)
    assert u is not None
    assert u.datas is None
    assert u.dates is None
    
    dt_start = '2023-02-24 09:30:00'
    dt_end = '2023-02-24 09:32:00'
    dt_start_obj = datetime.datetime.strptime(dt_start, "%Y-%m-%d %H:%M:%S")
    dt_end_obj = datetime.datetime.strptime(dt_end, "%Y-%m-%d %H:%M:%S")
    minutes_between_dates = dt_end_obj - dt_start_obj
    expected_rows_per_stock = divmod(minutes_between_dates.total_seconds(), 60)[0]+1
    
    u.load_universe_data_for_range(dt_start, dt_end)
    assert len(u.datas) == len(symbols) * expected_rows_per_stock
    
    #print('************************************************')
    #print(u.datas)
    #print(u.dates)
    #print('************************************************')
    print(f'\nExpected rows per stock: {expected_rows_per_stock}')
    print(f'Number of price rows loaded: {len(u.datas)}')
    print(f'Symbols requested {len(u.symbols_requested)}: {u.symbols_requested}')
    print(f"Dt start: {dt_start}, Dt end  : {dt_end}")
    print(f"Min date: {u.dt_min}, Max date: {u.dt_max}")





def test_json_universe_not_loaded():
    symbols = ['TSLA','AAPL','GIB-A.TO']
    u = TradeUniverse(symbols=symbols)
    json_dict = u.__json__()
    print(f'\nUniverse Json:{json_dict}')
    assert json_dict is None

def test_json_universe_loaded():
    symbols = ['TSLA','AAPL','GIB-A.TO']
    u = TradeUniverse(symbols=symbols)
    u.load_universe_data_all_dates()
    json_dict = u.__json__()
    assert json_dict is not None
    print(f'\nUniverse Json:{json_dict}')

def test__str__universe_loaded():
    symbols = ['TSLA','AAPL','GIB-A.TO']
    u = TradeUniverse(symbols=symbols)
    u.load_universe_data_all_dates()
    json_str = u.__str__()
    assert json_str is not None
    assert len(json_str) > 0
    print(f'\nJson_str: {json_str}')

def test__str__universe_not_loaded():
    symbols = ['TSLA','AAPL','GIB-A.TO']
    u = TradeUniverse(symbols=symbols)
    json_str = u.__str__()
    assert json_str is None
    print(f'\nJson_str: {json_str}')

def test_to_json_string_universe_loaded():
    symbols = ['TSLA','AAPL','GIB-A.TO']
    u = TradeUniverse(symbols=symbols)
    u.load_universe_data_all_dates()
    json_str = u.to_json()
    print(f'\nUniverse symbols: {u.loaded_symbols}')
    print(f'Json string (to_json): {json_str}')
    assert 'SymbolsNumber' in json_str

def test_to_json_string_universe_not_loaded():
    symbols = ['TSLA','AAPL','GIB-A.TO']
    u = TradeUniverse(symbols=symbols)
    json_str = u.to_json()
    print(f'\nUniverse symbols: {u.loaded_symbols}')
    print(f'Json string (to_json): {json_str}')
    assert json_str is None

def test_property_load_status_universe_loaded():
    symbols = ['TSLA','AAPL','GIB-A.TO']
    u = TradeUniverse(symbols=symbols)
    u.load_universe_data_all_dates()
    assert u.load_status
    
def test_property_load_status_universe_not_loaded():
    symbols = ['TSLA','AAPL','GIB-A.TO']
    u = TradeUniverse(symbols=symbols)
    assert not u.load_status

@pytest.mark.parametrize("symbols_to_check, expected", [
    (['TSLA','AAPL'], 2), 
    (['AAPL','TSLA'], 2),
    (['AAPL'], 1),
    (['TSLA','NoGood'], 1)
])
def test_property_found_in_db_and_loaded_symbols(symbols_to_check, expected):
    # found_in_db()
    # loaded_symbols()
    symbols = symbols_to_check
    u = TradeUniverse(symbols=symbols)
    u.load_universe_data_all_dates()    
    found_in_db = u.found_in_db
    assert found_in_db == expected
    assert len(u.loaded_symbols) == expected
    print(f'\nNumber of symbols in DB: {found_in_db}')
    print(f'Loaded symbols: {u.loaded_symbols}')
