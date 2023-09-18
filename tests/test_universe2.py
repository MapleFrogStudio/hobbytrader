'''Test script for TradeUniverse. Assumes example/build_db was run and roduced a database called DB/minute.sqlite'''
import pytest
from hobbytrader.universe2 import TradeUniverse

@pytest.fixture()
def not_loaded_universe():
    symbols = ['TSLA','AAPL']
    #symbols = ['AAPL', 'TSLA']
    u = TradeUniverse(symbols, load_data=False)    
    return symbols, u

@pytest.fixture()
def loaded_universe():
    symbols = ['TSLA','AAPL']
    u = TradeUniverse(symbols, load_data=True)    
    return symbols, u

@pytest.fixture()
def empty_universe():
    symbols = ['NoGood1','NoGood2']
    u = TradeUniverse(symbols, load_data=False)    
    return symbols, u

@pytest.fixture()
def partial_universe():
    symbols = ['TSLA','AAPL', 'NoGood']
    u = TradeUniverse(symbols, load_data=True)    
    return symbols, u



# SERIES OF TESTS TO CHECK contrutor without loading all the data
def test_TradeUniverse_constructor_no_parameters():
    with pytest.raises(TypeError):
        u = TradeUniverse()

def test_TradeUniverse_constructor_with_list():
    db = 'DB/minute.sqlite'
    symbols = ['AAPL','TSLA']
    u = TradeUniverse(symbols, load_data=False, db_path=db)
    assert u is not None
    assert u.db_path == db
    assert u.datas is None
    assert u.load_status == TradeUniverse.TU_DATA_LOADED_FAIL
    assert len(u.symbols_requested) == 2


def test_TradeUniverse_constructor_with_string():
    u = TradeUniverse('TSLA', load_data=False)
    assert u is not None

@pytest.mark.parametrize("non_strings_list",[
    (['TSLA',1]), (1,'TSLA'), ('TSLA',True)
])
def test_TradeUniverse_constructor_non_string_in_list(non_strings_list):
    with pytest.raises(ValueError):
        u = TradeUniverse(non_strings_list, load_data=False)

def test_TradeUniverse_constructor_load_data_non_boolean():
    with pytest.raises(ValueError):
        u = TradeUniverse(['TSLA','AAPL'], load_data=10)

def test_TradeUniverse_constructor_db_path_non_string():
    with pytest.raises(ValueError):
        u = TradeUniverse(['TSLA','AAPL'], db_path=10)


# TEST UNIVERSE with data loading and all stats
def test_load_full_universe(loaded_universe):
    symbols, u = loaded_universe

    assert u is not None
    assert u.symbols_requested == symbols
    assert u.loaded_symbols.sort() == symbols.sort()
    assert u.load_status == TradeUniverse.TU_DATA_LOADED_SUCCESS
    assert u.datas is not None

def test_partial_load_full_universe():
    db = 'DB/minute.sqlite'
    symbols = ['AAPL','TSLA', 'NoGood']
    u = TradeUniverse(symbols, load_data=True, db_path=db)
    assert u.load_status == TradeUniverse.TU_DATA_LOADED_PARTIAL    

# SERIES OF TESTS to check TradeUniverse methods
@pytest.mark.parametrize("symbols_to_check, expected", [
    (['NoGood1', 'NoGood2'], 0),
    (['TSLA','AAPL'], 2), 
    (['AAPL','TSLA'], 2),
    (['AAPL'], 1),
    (['TSLA','NoGood'], 1),
    ([], 0)
])
def test_symbols_exist_in_db(symbols_to_check, expected):
    u = TradeUniverse(symbols_to_check, load_data=False) # Only create the class do not load anything
    found_in_db = u.found_in_db
    print(f'Check_status: {found_in_db}')
    print(f'Valid symbols: {u._valid_symbols}')
    assert found_in_db == expected
    

def test_load_symbols_data_from_db(not_loaded_universe):
    _, u = not_loaded_universe
    found_in_db = u.found_in_db
    assert u is not None
    assert found_in_db > 0
    # We are ready to test our load function (we now assume our symbols are in DB)
    u.load_universe_data()
    assert u.datas is not None

def test_fail_load_symbols_data_from_db(empty_universe):
    symbols, u = empty_universe
    u.load_universe_data()
    assert u.load_status == TradeUniverse.TU_DATA_LOADED_FAIL
    assert u.datas == None
    assert u.loaded_symbols is None
    assert u.dt_min is None
    assert u.dt_max is None
    print(f'Found in DB: {u.found_in_db}')

def test_properties_with_loaded_data(loaded_universe):
    symbols, u = loaded_universe
    assert u.load_status is not None
    assert u.found_in_db == len(symbols)
    assert len(u.loaded_symbols) == len(symbols)
    assert u.dt_min is not None
    assert u.dt_max is not None

def test_prices_for_date(loaded_universe):
    symbols, u = loaded_universe
    dt = u.dt_min
    print(f'----------------- Min date : {dt}')
    price_rows = u.prices_for_date(dt)
    assert len(price_rows) == len(symbols)

def test_fail_prices_for_date(loaded_universe):
    _, u = loaded_universe
    result = u.prices_for_date(None)
    assert result is None

def test_prices_for_dates(loaded_universe):
    symbols, u = loaded_universe
    dt1 = u.dates[0]
    dt2 = u.dates[1]
    print(f'----------------- Date1: {dt1}, Date2: {dt2}')
    price_rows = u.prices_for_dates(dt1, dt2)
    assert len(price_rows) == len(symbols)*2    

def test_fail_prices_for_dates(loaded_universe):
    symbols, u = loaded_universe
    dt1 = u.dates[0]
    dt2 = u.dates[1]
    result1 = u.prices_for_dates(None, None)
    assert result1 is None
    result2 = u.prices_for_dates(None, dt2)
    assert result2 is None
    result3 = u.prices_for_dates(dt1, None)
    assert result3 is None
    result4 = u.prices_for_dates(dt2, dt1)
    assert result4 is None

def test_symbol_by_id(loaded_universe):
    symbols, u = loaded_universe
    symbols.sort()
    symbol_id = 1
    returned_symbol = u.symbol_by_id(symbol_id)
    print(f'\nSymbol chosen: {symbol_id}')
    print(f'Returned symbol: {returned_symbol}')
    print(f'loaded symbols: {u.loaded_symbols}')
    assert returned_symbol == symbols[symbol_id]

def test_symbols_by_id_not_an_int(loaded_universe):
    symbols, u = loaded_universe
    returned_symbol = u.symbol_by_id('notint')
    assert returned_symbol is None

def test_symbols_by_id_out_of_range(loaded_universe):
    symbols, u = loaded_universe
    returned_symbol = u.symbol_by_id(len(u.loaded_symbols))
    assert returned_symbol is None
    
def test_id_by_symbol(loaded_universe):
    symbols, u = loaded_universe
    symbols.sort()
    id = 1
    symbol = symbols[id]

    returned_id = u.id_by_symbol(symbol)
    print(f'\nSymbol chosen: {symbol}, for id:{id}')
    print(f'Returned symbol: {returned_id}')
    print(f'loaded symbols: {u.loaded_symbols}')
    assert returned_id == id

def test_id_by_symnol_not_a_string(loaded_universe):
    symbol, u = loaded_universe
    not_a_string = 10
    id = u.id_by_symbol(not_a_string)
    assert id == None

def test_id_by_symbol_not_found(loaded_universe):
    symbol, u = loaded_universe
    not_foud_symbol = 'NoGood'
    id = u.id_by_symbol(not_foud_symbol)
    assert id == None

def test_date_properties(loaded_universe):
    symbols, u = loaded_universe
    print(f'\nLoaded universe, date value: {u.date}')
    print(f'Loaded universe, date index: {u.date_index}')
    assert u.date == u.dates[0]
    assert u.date_index == 0
    success1 = u.next_dt()
    print(f'\nLoaded universe, date value: {u.date}')
    print(f'Loaded universe, date index: {u.date_index}')
    assert success1
    assert u.date == u.dates[1]
    assert u.date_index == 1
    success2 = u.prev_dt()
    print(f'\nLoaded universe, date value: {u.date}')
    print(f'Loaded universe, date index: {u.date_index}')
    assert success2
    assert u.date == u.dates[0]
    assert u.date_index == 0
    assert u.prev_dt() is False  # Current date is already at index 0

def test_date_index_no_dates_loaded(empty_universe):
    _, u = empty_universe
    u.dt_current = None # Force an incohernt config
    returned_index = u.date_index
    assert returned_index is None

def test_date_index_setter(loaded_universe):
    _, u = loaded_universe
    print(f'\nCurrent default date: {u.date}')
    print(f'Current date index: {u.date_index}')
    new_index = 60 # One hour later
    u.date_index = new_index
    assert u.date_index == new_index
    print(f'New date: {u.date}')
    print(f'New date_index: {u.date_index}')
    u.date_index = -1
    assert u.date_index == 0
    u.date_index = len(u.dates)
    assert u.date_index == len(u.dates) - 1

def test_next_dt_on_last_index(loaded_universe):
    symbols,u = loaded_universe
    last_date_index = len(u.dates)-1
    u.date_index = last_date_index
    print(f'\nCurrent date: {u.date}, at index: {u.date_index} where total dates: {len(u.dates)}')
    success = u.next_dt()
    assert not success

def test_json_returned(loaded_universe):
    symbols,u = loaded_universe
    json_dict = u.__json__()
    print(f'\nUniverse Json:{json_dict}')
    assert json_dict is not None

def test_json_empty_universe(empty_universe):
    symbols,u = empty_universe
    json_dict = u.__json__()
    print(f'\nUniverse Json:{json_dict}')
    assert json_dict is None

def test_json_partial_universe(partial_universe):
    symbols,u = partial_universe
    json_dict = u.__json__()
    print(f'\nUniverse Json:{json_dict}')
    assert json_dict is not None

def test_to_json_string_returned(loaded_universe):
    symbols,u = loaded_universe
    json_str = u.to_json()
    print(f'Universe symbols: {u.loaded_symbols}')
    print(f'Json string (to_json): {json_str}')
    assert 'SymbolsNumber' in json_str

def test_fail_to_json_string_returned(empty_universe):
    symbols,u = empty_universe
    json_str = u.to_json()
    print(f'Universe symbols: {u.loaded_symbols}')
    print(f'Json string (to_json): {json_str}')
    assert json_str is None

def test__str__loaded(loaded_universe):
    symbols,u = loaded_universe
    json_str = u.__str__()
    print(json_str)

def test_fail__str__loaded(empty_universe):
    symbols,u = empty_universe
    json_str = u.__str__()
    print(json_str)    
    assert json_str is None
