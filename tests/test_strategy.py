import pytest
from hobbytrader import yahoo, strategy

def test_setup_multi_asset():
    symbols = ['TSLA','MSFT','AAPL']
    data_df = yahoo.yahoo_prices(symbols, '2023-03-27')
    assert data_df is not None
    multi_list = strategy.setup_multi_asset(data_df)
    assert multi_list is not None
    assert len(multi_list) == len(symbols)

def test_setup_multi_asset_fail_no_symbol():
    symbols = ['TSLA','MSFT','AAPL']
    data_df = yahoo.yahoo_prices(symbols, '2023-03-27')
    # Remove the symbol column from Dataframe
    data_df = data_df[['Open','High','Low','Close','Volume']]
    with pytest.raises(Exception):
        multi_list = strategy.setup_multi_asset(data_df)
