import pytest
from hobbytrader import scrapper

testdata = [
    ('tsx'   , 'canada'),
    ('tsxv'  , 'canada'),
    ('nasdaq', 'usa'   ),
    ('nyse', 'usa'   ),
]

@pytest.mark.parametrize("exchange,country", testdata)
def test_scrap_advfn(exchange, country):
    #exchange = 'tsx'
    #country = 'canada'
    symbols_df = scrapper.scrap_advfn(exchange, country)
    assert symbols_df is not None
