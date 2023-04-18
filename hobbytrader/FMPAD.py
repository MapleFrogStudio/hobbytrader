# Financial Modeling Prep API Documentation
# https://site.financialmodelingprep.com/developer/docs/
import os
import json
import certifi
import pandas as pd

from urllib.request import urlopen
from dotenv import load_dotenv

load_dotenv()

def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)




api_key = os.getenv('FMPAD_API_KEY')
print(api_key)

symbol = 'nyse'
#url = f'https://financialmodelingprep.com/api/v3/income-statement/{symbol}?apikey={api_key}'
#url = f'https://financialmodelingprep.com/api/v3/quotes/{symbol}?apikey={api_key}'
#url = f'https://financialmodelingprep.com/api/v3/historical-chart/1min/{symbol}?apikey={api_key}'
url =  f'https://financialmodelingprep.com/api/v3/historical-chart/1min/AAPL?apikey=adccbf975492ed7c363f12ed8d7f3ded'
data = get_jsonparsed_data(url)
print(type(data))
print(data[0:3])
data_df = pd.DataFrame(data)
print(data_df.head(3))
