import requests
import re
import io
import pandas as pd

class Github:
    """Utility class to retrieve github info and links"""

    def __init__(self, owner='MapleFrogStudio', repository='DATASETS', branch='main'):
        self.owner = owner
        self.repo  = repository
        self.branch = branch

    def __repr__(self):
        return(f'{self.owner} -> {self.repo} -> {self.branch}')

    @property
    def url(self):
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/contents/'
        return url
    
    def url_path(self, folder='/'):
        if folder == '/' or folder == '' or folder is None:
            return self.url
        
        return self.url+folder


    def file_links(self, folder='/', starts_with=''):
        ''' Return a list of files from  github repo that start_with a specifc string '''
        url = self.url_path(folder=folder)

        content = requests.get(url)
        data = content.json()
        
        if isinstance(data, list):
            if starts_with == '' or starts_with is None:
                raw_urls = [record['download_url'] for record in data if record['type'] == 'file']
            else:
                pattern = pattern = r"^" + starts_with + r".*\.csv$"
                raw_urls = [record['download_url'] for record in data if record['type'] == 'file' and re.match(pattern, record['name'])]

            return raw_urls
        else:
            return []




def grab_SP500_from_wikipedia():
    # wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks'
    wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    s = requests.get(wiki_url).content
    tickers = pd.read_html(io.StringIO(s.decode("utf-8")))
    tickers_df = tickers[0]
    tickers_df['Yahoo'] = [s.replace('.', '-') for s in tickers_df.Symbol]
    return tickers_df

def grab_SP500_history_from_wikipedia():
    wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    s = requests.get(wiki_url).content
    history = pd.read_html(io.StringIO(s.decode("utf-8")))
    history_df = history[1]
    history_df = history_df.reset_index()

    history_df.columns = [f'{level1}_{level2}' if level2 else level1 for level1, level2 in history_df.columns]
    history_df.rename(columns={'Date_Date': 'Date'}, inplace=True)
    history_df.drop(columns='index', inplace=True)

    return history_df

def grab_SP500_from_github_mfs_dataset() -> pd.DataFrame:
    url = "https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO/sp500.csv"
    tickers_df = pd.read_csv(url, header=0, index_col=None)
    tickers_df['Yahoo'] = [s.replace('.', '-') for s in tickers_df.Symbol]
    return tickers_df

def grab_tsx_stocks_from_github_mfs_dataset() -> pd.DataFrame:
    url = "https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO/tsx.csv"
    tickers_df = pd.read_csv(url, header=0, index_col=None, keep_default_na=False)
    tickers_df['Yahoo'] = [f"{s.replace('.', '-')}.TO" for s in tickers_df.Symbol]
    tickers_df = tickers_df.loc[tickers_df.Type == 'EQUITY']
    
    return tickers_df

def grab_nasdaq_sector_from_github_mfs_dataset(sector='Energy') -> pd.DataFrame:
    # sectors = ['', 'Consumer Defensive', 'Financial Services', 'Healthcare', 'Industrials', 'Technology', 'Consumer Cyclical', 'Basic Materials', 'Utilities', 'Communication Services', 'Real Estate', 'Energy']
    nasdaq_url = 'https://raw.githubusercontent.com/MapleFrogStudio/DATASETS/main/STOCK_SYMBOLS/YAHOO/nasdaq.csv'
    nasdaq_df = pd.read_csv(nasdaq_url, header=0, index_col=None, keep_default_na=False)
    nasdaq_df.rename(columns={'YahooTicker':'Yahoo'}, inplace=True)
    sector_df = nasdaq_df.loc[nasdaq_df.Type == 'EQUITY'].copy()
    sector_df = sector_df.loc[sector_df.Sector == sector].copy()
    return sector_df