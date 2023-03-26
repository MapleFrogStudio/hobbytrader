# Maple Frog Studio - Hobby Trader Package 
>**Warning**  
>Work in progress, not production ready, poor documentation :)  
>No user interface, all demos run from the command line with results printed in the terminal
## Hobby trader is a python project for manipulating historical price data for stock trading  
  
This project is divided into three (3) repository:
- [hobbytrader](https://github.com/MapleFrogStudio/hobbytrader) : repository with programs to create autoated strategies and backtest  
- [downloader](https://github.com/MapleFrogStudio/downloader) : repository with github actions to download dialy minute price data  
- [DATASET](https://github.com/MapleFrogStudio/DATASETS) : repository to store accumulated data for later use in backtesting  

# Downloader
This project uses github actions to download daily minute price data and archive the results as a CSV or PARQUET file. The generated files cover the following groups of symbols:
* TSX
* S&P500
* Each sector (CS - Consumer Defensive, FS - Financial Services, HC - Healthcare, IN - Industrials, TE - technology, CC - Consumer Cyclical, BM - Basic Materials, UT - Utilisities, CS - Communication Services, RE - Real Estate, EN - Energy)

# Modules 
  
**More to comme...**

# Limitations
- Lists of symbols come from statc symbols files that are updated on a random frequency
- Minuet Price Data are stored in blocks of symbols to helps keep files under Github limitations

# Installation
Open a command shell (powershell) and run the commands lines below
- Requires python 3.11 or higher so [Download](https://www.python.org/downloads/) latest version to upgrade your python environment
- Clone the repository to your local folder
- Create a python virtual envirnnement (suggested venv module that comes with python install)
- Upgade your PIP installations and install dependencies
- Pip install the package dependences
- Run our check_install python script

```  
> python --version  
> git clone git@github.com:MapleFrogStudio/hobbytrader.git hobbytrader
> cd hobbytrader
> python -m venv env
> .\env\Scripts\Activate  
> python -m pip install --upgrade pip
> pip install -e .
```
## Commands  
To download he latest trading day's minute price for the TSX, luanch tsx from the command line. A CSV file wil be created in teh DATASET local folder
> tsx  
* See the pyproject.toml file for other predefined commands
  
## Tests  
Run all tests in your environment using the following command (some tests might be longer than 1 minute)  
>pytest -v  

## Examples  
Run examples from the root directory of your projet
```
> python .\examples\symbols_github.py  
> python .\examples\symbols_sp500.py  
```

## Possible Data sources to investigate
[NASDAQ Stock Screener](https://www.nasdaq.com/market-activity/stocks/screener) to download csv files  
[ADVFN](https://ca.advfn.com/investing/stocks/canada/tsx?letter=A)
[Alpha Vantage](https://www.alphavantage.co/documentation/#listing-status) to download csv files of listed & delisted stock symbols
[Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs/) 

