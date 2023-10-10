import pytest
import pandas as pd

from hobbytrader import github

def test_init_defaults():
    github_object = github.Github()
    assert github_object.owner == 'MapleFrogStudio'
    assert github_object.branch == 'main'

def test__repr():
    github_object = github.Github()
    result = github_object.__repr__()
    assert result == 'MapleFrogStudio -> DATASETS -> main'


def test_github_setup():
    repo = 'DATA-2023-06-02'
    github_object = github.Github(repository=repo)
    assert github_object.repo == repo

def test_url():
    url = 'https://api.github.com/repos/MapleFrogStudio/DATASETS/contents/'
    github_object = github.Github()
    #print(github_object.url)
    assert github_object.url == url

def test_url_path():
    github_object = github.Github()
    url_path = github_object.url_path('DAILY')
    print(url_path)
    assert url_path == 'https://api.github.com/repos/MapleFrogStudio/DATASETS/contents/DAILY'

def test_file_links():
    github_object = github.Github(repository='DATA-2023-06')
    files = github_object.file_links(starts_with='NASDAQ-BM0')
    # print(type(files))
    assert len(files) > 1

def test_files_links_bad_subfolder():
    github_object = github.Github(repository='DATA-2023-06')
    files = github_object.file_links(folder='bad_folder')
    assert len(files) == 0

def test_file_links_without_starts_with():
    github_object = github.Github(repository='DATA-2023-06')
    files = github_object.file_links(starts_with=None)
    assert len(files) >= 0


def test_grab_SP500_from_wikipedia():
    results_df = github.grab_SP500_from_wikipedia()
    number_of_items = len(results_df)
    assert results_df is not None
    assert 499 < number_of_items < 505
    assert 'GOOG' in results_df.Symbol.to_list()

def test_grab_SP500_from_github_mfs_dataset():
    results_df = github.grab_SP500_from_github_mfs_dataset()
    number_of_items = len(results_df)
    assert results_df is not None
    assert number_of_items > 499
    assert 'GOOG' in results_df.Symbol.to_list()

def test_grab_tsx_stocks_from_github_mfs_dataset():
    results_df = github.grab_tsx_stocks_from_github_mfs_dataset()
    symbol_types = results_df.Type.unique()
    assert results_df is not None
    assert len(symbol_types) == 1
    assert symbol_types[0] == 'EQUITY'
    assert 'GIB.A' in results_df.Symbol.to_list()

def test_grab_nasdaq_sector_from_github_mfs_dataset():
    # Call with default sector
    results_df = github.grab_nasdaq_sector_from_github_mfs_dataset()
    assert results_df is not None

def test_grab_nasdaq_sector_from_github_mfs_dataset_tech():
    # Call with a sector passed as argument
    results_df = github.grab_nasdaq_sector_from_github_mfs_dataset(sector='Technology')
    assert results_df is not None

def test_compare_sp500_git_vs_wikipedia():
    wikipedia_symbols = github.grab_SP500_from_wikipedia()['Symbol'].tolist()
    github_symbols = github.grab_SP500_from_github_mfs_dataset()['Symbol'].tolist()
    print(wikipedia_symbols)
    print('----')
    print(github_symbols)
    print('Symbols in wiki not in github')
    difference = list(set(wikipedia_symbols) - set(github_symbols))
    print(difference)
    print('Symbols in github not in wiki')
    difference = list(set(github_symbols) - set(wikipedia_symbols))
    print(difference)  
    assert True

def test_grab_SP500_history():
    data = github.grab_SP500_history_from_wikipedia()
    assert isinstance(data, pd.DataFrame)
    print('---')
    print(data)
    print(data.columns)
          