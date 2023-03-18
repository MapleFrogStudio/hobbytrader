from hobbytrader import symbols

def test_grab_SP500_from_wikipedia():
    results_df = symbols.grab_SP500_from_wikipedia()
    number_of_items = len(results_df)
    assert results_df is not None
    assert 499 < number_of_items < 505
    assert 'GOOG' in results_df.Symbol.to_list()

def test_grab_SP500_from_github_mfs_dataset():
    results_df = symbols.grab_SP500_from_github_mfs_dataset()
    number_of_items = len(results_df)
    assert results_df is not None
    assert number_of_items > 499
    assert 'GOOG' in results_df.Symbol.to_list()

def test_grab_tsx_stocks_from_github_mfs_dataset():
    results_df = symbols.grab_tsx_stocks_from_github_mfs_dataset()
    symbol_types = results_df.Type.unique()
    assert results_df is not None
    assert len(symbol_types) == 1
    assert symbol_types[0] == 'EQUITY'
    assert 'GIB.A' in results_df.Symbol.to_list()

def test_grab_nasdaq_sector_from_github_mfs_dataset():
    # Call with default sector
    results_df = symbols.grab_nasdaq_sector_from_github_mfs_dataset()
    assert results_df is not None

def test_grab_nasdaq_sector_from_github_mfs_dataset_tech():
    # Call with default sector
    results_df = symbols.grab_nasdaq_sector_from_github_mfs_dataset(sector='Technology')
    assert results_df is not None
