import pytest
import os
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

from hobbytrader.scrappers import Scrapper, ADVFN, FMPAD

FAKE_DATA = {
    'Symbol': ['AW.UN', '7745', 'ABCT'],
    'Close' : ['123.23', '999.98', '983.12']
}

def test_Scrapper_class_uninstantiable():
    with pytest.raises(TypeError):
        s = Scrapper()

def test_ADVFN_class_init():
    s = ADVFN()
    assert s.country == 'canada'
    assert s.exchange == 'tsx'


def test_ADVFN_letters_list():
    s = ADVFN()    
    letters = s.letters_list()
    assert len(letters) == 27

def test_ADVFN_extract_all_lines_with_symbol_inf():
    s = ADVFN(exchange='nasdaq', country='usa')
    full_url = s.url_base + 'A'
    lines_with_symbol_info = s.extract_all_lines_with_symbol_info(full_url)
    assert isinstance(lines_with_symbol_info, list)
    assert len(lines_with_symbol_info) > 0
    print(lines_with_symbol_info[0])

def test_ADVFN_bad_extract_all_lines_with_symbol_inf():
    s = ADVFN(exchange='bad', country='usa')
    full_url = s.url_base + 'A'
    lines_with_symbol_info = s.extract_all_lines_with_symbol_info(full_url)
    assert isinstance(lines_with_symbol_info, list)
    assert len(lines_with_symbol_info) == 0    

def test_ADVFN_extract_name_and_symbo():
    s = ADVFN()
    full_url = s.url_base + 'A'
    lines_with_symbol_info = s.extract_all_lines_with_symbol_info(full_url)
    tag_element = lines_with_symbol_info[0]
    extracted_info = s.extract_name_and_symbol(tag_element)
    print(extracted_info)
    assert 'Symbol' in extracted_info.keys()
    assert 'Name' in extracted_info.keys()
    assert 'Url' in extracted_info.keys()

def test_ADVFN_scrape_data():
    s = ADVFN()
    symbols = s.scrape_data()
    print(symbols)
    assert len(symbols) > 0

def test_ADVFN_add_yahoo_symbols():
    fake_df = pd.DataFrame(FAKE_DATA)
    print('---')
    print(f'Print fake_data:\n{fake_df}')
    fake_df = ADVFN().add_yahoo_symbol(fake_df)
    print(f'Print fake_data:\n{fake_df}')
    assert 'Yahoo' in fake_df.columns

def test_ADVFN_to_csv():
    # Default filename : advfn-tsx.csv
    fake_df = pd.DataFrame(FAKE_DATA)
    ADVFN().to_csv(fake_df)
    csv_filename = './advfn-tsx.csv'
    assert os.path.isfile(csv_filename)
    os.remove(csv_filename)

@pytest.fixture(scope="session")
def api_key_value():
    api_key = os.getenv('FMPAD_API_KEY')
    return api_key

def test_FMPAD_api_key_defined(api_key_value):
    #api_key = os.getenv('FMPAD_API_KEY')
    api_key = api_key_value
    assert api_key is not None
    assert len(api_key) > 10

def test_FMPAD_class_init(api_key_value):
    f = FMPAD()
    assert f is not None
    assert f.api_key == api_key_value
    assert f.url_base is not None
    assert isinstance(f.url_base, str)

def test_FMPAD_rename_columns():
    mock ={
        "symbol":['unused','unused','unused'],
        "companyName":['unused','unused','unused'],
        "marketCap":['unused','unused','unused'],
        "sector":['unused','unused','unused'],
        "industry":['unused','unused','unused'],
        "beta":['unused','unused','unused'],
        "price":['unused','unused','unused'],
        "lastAnnualDividend":['unused','unused','unused'],
        "volume":['unused','unused','unused'],
        "exchange":['unused','unused','unused'],
        "exchangeShortName":['unused','unused','unused'],
        "country":['unused','unused','unused'],
        "isEtf":['unused','unused','unused'],
        "isActivelyTrading":['unused','unused','unused'],
        }
    data_df = pd.DataFrame(mock)
    f = FMPAD()
    data_df = f.rename_columns(data_df)
    assert 'Symbol' in data_df.columns
    assert 'Name' in data_df.columns
    assert 'Sector' in data_df.columns
    assert 'Volume' in data_df.columns
    assert 'IsActivelyTrading' in data_df.columns

def test_FMPAD_get_jsonparsed_data():
    f = FMPAD()
    data_df = f.get_jsonparsed_data()
    assert data_df is not None
    assert isinstance(data_df, pd.DataFrame)
    assert len(data_df.columns) == 14
    print(data_df)
    print(data_df.columns)

def test_FMPAD_scrape_data():
    f = FMPAD()
    data_df = f.scrape_data()
    assert 'Yahoo' in data_df.columns