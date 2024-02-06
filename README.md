# Maple Frog Studio - Hobby Trader Package 
>**Warning**  
>Work in progress, not production ready, poor documentation :)  
>No user interface, all demos run from the command line with results printed in the terminal
## Hobby trader is a python project for manipulating historical price data for stock trading  
  
This project is divided into three (3 or more) repositories:
- [hobbytrader](https://github.com/MapleFrogStudio/hobbytrader) : repository with programs to create automated strategies and backtests  
- [downloader](https://github.com/MapleFrogStudio/downloader) : repository with github actions to download daily minute price data (2023 symbols list)  
- [downloader2024](https://github.com/MapleFrogStudio/downloader2024) : repository with github actions to download daily minute price data (2024 symbols list)  
- [DATASETS](https://github.com/MapleFrogStudio/DATASETS) : repository to store accumulated data for later use in backtesting (*some SP500 & some TSX*)    
- Other repositories [DATA-9999-99] containing monthly minute price data for other exchanges (example June 2023 -> DATA-2023-06) symbols stored in csv files may vary from one month to the next    
  

# High level view of package components
![High level module schema](hobbytrader\assets\hobbytrader01.png)


# Downloader repos 
These projects [2023](https://github.com/MapleFrogStudio/downloader) / [2024](https://github.com/MapleFrogStudio/downloader2024) use github actions to download daily minute price data and archive the results as a CSV file. The list of symbols is managed manually and saved to different github repos. 

# Limitations
- Lists of tickers come from static symbols files that are updated on a random/yearly frequency  

# Installation
Open a command shell (powershell on windows) and run the command lines below
- Requires python 3.11 or higher so [Download](https://www.python.org/downloads/) latest version to upgrade your python environment
- Clone the repository to your local folder
- Create a python virtual environement (suggested venv module that comes with python install)
- Upgade your PIP installations and install dependencies
- Pip install the package dependencies
```  
> python --version  
> git clone git@github.com:MapleFrogStudio/hobbytrader.git hobbytrader
> cd hobbytrader
> python -m venv env
> .\env\Scripts\Activate  
> python -m pip install --upgrade pip
> pip install -e .
```
### Package configuration
Some environment variables must ne setup for proper package usage. If working in a local environment create a .env file in the root folder of your project and add the following lines:  
```  
FMPAD_API_KEY=somerandomkeyfromFFPAD
DB_SQL_LIMIT = 1000  # 0 no limits applied to SQL Requests
```
<sup><sub>*FMPAD API KEY must be obtained from [FMPAD](https://site.financialmodelingprep.com/developer/docs/) website and click get my API KEY here*</sub></sup>
   
## Commands  
To download the latest trading day's minute prices for the TSX, launch tsx from the command line. A CSV file will be created in the DATASET local folder
> tsx  
* See the pyproject.toml file for other predefined commands

# Modules 
  
| Module | Description |
| --- | --- |
| github.py   | Class with Helper methods to get filenames and download links from github repos using owner and repo names |
| scrappers.py |  Web Scrapper to download company symbols (tickers) from different web sites ([ADVFN](https://www.advfn.com/investing/stocks/canada/tsx?letter=A) & [FMPAP]((https://site.financialmodelingprep.com/developer/docs/)))|
| database.py |  Functions to download price data from github repo and generate a SQLITE3 database (also supports CSV and Parquet save) |
| yahoo.py | Function wrappers around the yfinance package to download daily or minute price data for lists of stock symbols |
| download.py | Functions to automate downloading price data from yahoo finance and storing them as CSV and Parquet files (*called from github actions*) |


## Tests  
Run all tests with [pytest](https://docs.pytest.org/en) and code [coverage](https://pytest-cov.readthedocs.io/en/latest/) in your environment using the following command (some tests might be longer than 1 minute)  
```
coverage erase  
coverage run -m pytest -v  
coverage report -m  
```  
The last line will show a report of code coverage by all defined tests in the project indicating if some lines have not been tested

## Examples  
Run examples from the root directory of your projet
```
python .\examples\symbols_github.py  
python .\examples\symbols_sp500.py  
python .\examples\build_db.py  
python .\examples\read_from_db.py  
```
**build_db.py** a script to download csv minute price data from MapleFrogStudio's stored data to save as a SQLITE3 database.  
Adjust the following parameters for your specific needs:  
- repo = 'DATASETS' (github repo you want to download from)  
- subfolder = '/DAILY' (the subfolder where the csv files are stored in the repo)
- starts_with = 'TSX-' (The filter to use only the files that start with...)  

Notes: The example uses a little SQL hack to create a fake index combining the Datetime and Symbol to filter out duplicate lines when saving to the database. 

## Designer tool (PyQt6)  
```
.\env\Scripts\pyqt6-tools designer
```

## Possible Data sources to investigate
[NASDAQ Stock Screener](https://www.nasdaq.com/market-activity/stocks/screener) to download csv files  
[ADVFN](https://ca.advfn.com/investing/stocks/canada/tsx?letter=A)  
[Alpha Vantage](https://www.alphavantage.co/documentation/#listing-status) to download csv files of listed & delisted stock symbols  
[FMPAP - Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs/)  
[Free Forex minute data](http://www.histdata.com/)

