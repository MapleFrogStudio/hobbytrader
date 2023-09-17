import pytest
import pandas as pd
import io
import sys

from hobbytrader import view
from hobbytrader.database import load_OHLCV_from_db_for_symbols

@pytest.fixture(scope="session")
def load_ohlcv_data():
    db_file = 'DB/minute.sqlite'
    symbols_to_load = ['TSLA', 'AAPL']
    data = load_OHLCV_from_db_for_symbols(db_file, symbols_to_load)
    return data

def test_ConsolePrinter_init(load_ohlcv_data):
    data = load_ohlcv_data
    symbols_to_load = ['TSLA', 'AAPL']
    symbol_to_print = 'TSLA'
    console = view.ConsolePrinter(symbol_to_print, data)
    assert console is not None
    assert console.ticker == symbol_to_print
    assert len(console.ohclv_data.Symbol.unique()) == 1
    assert console.ohclv_data.Symbol.unique()[0] == symbol_to_print
    assert console.total_rows > 0
    assert console.current_index == 0
    assert isinstance(console.dates, list)

    print(f'Returned symbol: {console.ohclv_data.Symbol.unique()[0]}')
    print(f'First 50 dates: {console.dates[0:50]}')

def test_print_header(load_ohlcv_data):
    data = load_ohlcv_data
    symbol_to_print = 'TSLA'
    console = view.ConsolePrinter(symbol_to_print, data)
    console.print_header()

def test_row_values(load_ohlcv_data):
    data = load_ohlcv_data
    symbol_to_print = 'TSLA'
    console = view.ConsolePrinter(symbol_to_print, data)
    row_data = console.row_values()
    assert isinstance(row_data, pd.DataFrame)
    assert len(row_data) == 1
    assert 'Datetime' in row_data.columns
    assert 'Symbol'   in row_data.columns
    assert 'Open'     in row_data.columns
    assert 'High'     in row_data.columns
    assert 'Low'      in row_data.columns
    assert 'Close'    in row_data.columns
    assert 'Volume'   in row_data.columns

    print(row_data)
    print(type(row_data))

def test_print_row(load_ohlcv_data):
    data = load_ohlcv_data
    symbol_to_print = 'TSLA'
    console = view.ConsolePrinter(symbol_to_print, data)
    
    captured_header = io.StringIO()                 # Create StringIO object
    sys.stdout = captured_header                    #  and redirect stdout.
    console.print_header()
    sys.stdout = sys.__stdout__                     # Reset redirect.
    header_len = len(captured_header.getvalue())

    captured_row = io.StringIO()                    # Create StringIO object
    sys.stdout = captured_row                       #  and redirect stdout.
    console.print_row()
    sys.stdout = sys.__stdout__                     # Reset redirect.
    row_len = len(captured_row.getvalue())
    
    assert row_len == header_len

def test_next_date_stops_at_last_row(load_ohlcv_data):
    data = load_ohlcv_data
    symbol_to_print = 'TSLA'
    console = view.ConsolePrinter(symbol_to_print, data)
    i = 1
    while console.next_date():
        i += 1
    assert i == console.total_rows

