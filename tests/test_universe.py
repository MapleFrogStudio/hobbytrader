import pytest
import pandas as pd

from hobbytrader.universe import TradeUniverse

@pytest.fixture(scope="session")
def test_data():        
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

@pytest.fixture(scope="session")
def test_one_symbol():
    ID =     ['20230428093000AMZN','20230428093100AMZN','20230428093200AMZN','20230428093300AMZN','20230428093400AMZN']
    Dates =  ['2023-04-28 09:30:00','2023-04-28 09:31:00','2023-04-28 09:32:00','2023-04-28 09:33:00','2023-04-28 09:34:00']
    Symbols= ['AMZN','AMZN','AMZN','AMZN','AMZN']
    Close =  [268.910995483398,268.720001220703,268.71009826660,268.365005493164,268.509994506836]
    High =   [269.039993286133,268.960006713867,268.83999633789,268.710006713867,268.672607421875]
    Low =    [268.259994506836,268.679992675781,268.53010559082,268.339996337891,268.369995117188]
    Open =   [268.490005493164,268.910003662109,268.72000122070,268.710006713867,268.369995117188]
    Volume = [2030045.0, 268035.0, 261020.0, 210307.0, 213959.0]

    df = pd.DataFrame({
        'Datetime': Dates, 'Symbol': Symbols, 'Close': Close, 'High': High, 'Low': Low, 'Open': Open, 'Volume': Volume
    })
    return df.copy()



def test_TradeUniverse_init():
    # Test with module fake data
    u = TradeUniverse(datas=None)
    assert u is not None
    assert u.fake_data is True
    assert u.dates is not None
    assert len(u.symbols) == 2

def test_TradeUniverse_with_data(test_data):
    u = TradeUniverse(datas=test_data)
    assert u is not None
    assert u.fake_data is False
    assert u.dates is not None
    assert len(u.symbols) == 2    

def test_TradeUniverse_no_dataframe():
    invalid_data = ['item1','item2']
    u = TradeUniverse(datas=invalid_data)
    assert u is not None

def test_TradeUniverse_with_bad_data(test_data):
    bad_data = test_data.drop(columns=['Volume'])
    with pytest.raises(TypeError):
        u = TradeUniverse(datas=bad_data)

def test_valid_price_columns_fail(test_data):
    bad_data = test_data.drop(columns=['Volume'])
    bad_data['fake_col1'] = None
    bad_data['fake_col2'] = None
    bad_data['fake_col3'] = None
    u = TradeUniverse(test_data) # Create a TradeUniverse object with valid info
    validation = u.valid_price_columns(bad_data)
    assert validation == False

def test_valid_price_columns_no_dataframe(test_data):
    u = TradeUniverse(test_data) # Create a TradeUniverse object with valid info
    not_a_dataframe = ['invalid_item']
    validation = u.valid_price_columns(not_a_dataframe)
    assert validation == False

def test__json___dict_returned(test_data):
    u = TradeUniverse(test_data)
    json_dict = u.__json__()
    assert json_dict is not None
    assert isinstance(json_dict, dict)

def test__str__returned_string(test_data):
    u = TradeUniverse(test_data)
    result = u.__str__()
    assert result is not None
    assert isinstance(result, str)

def test_to_json_returned_string(test_data):
    u = TradeUniverse(test_data)
    result = u.to_json()
    assert result is not None
    assert isinstance(result, str)

def test_symbol_by_id(test_data):
    u = TradeUniverse(datas=test_data)
    assert u.symbol_by_id(0) == 'AAPL'
    assert u.symbol_by_id(4) is None
    assert u.symbol_by_id('not an int') == None

def test_id_by_symbol(test_data):
    u = TradeUniverse(datas=test_data)
    assert u.id_by_symbol('AAPL') == 0
    assert u.id_by_symbol('NonExistant') == None
    not_a_string = 10
    assert u.id_by_symbol(not_a_string) == None

def test_add_datas_bad_parameter(test_data):
    u = TradeUniverse(test_data)
    not_a_dataframe = ['item1']
    with pytest.raises(AttributeError):
        u.add_datas(not_a_dataframe)

def test_add_datas_one_symbol(test_data, test_one_symbol):
    u = TradeUniverse(test_data)
    #u.add_datas(test_one_symbol)
    #assert len(u.symbols) == 3