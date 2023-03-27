import pytest
import os
import pandas as pd
from hobbytrader import database

testdata = [
    ('TSX'   ),
    ('NASDAQ'),
    ('SP500'  ),
]

@pytest.mark.parametrize("base_name", testdata)
def test_filenames_from_github_repo(base_name):
    filenames = database.filenames_from_github_repo(base_name)
    assert len(filenames) > 0

def test_create_db_and_table():
    test_file = 'testdb.sqlite3'
    db_connection = database._create_db_and_table(test_file)
    assert db_connection is not None
    # Try to insert the same data twice to check if create DB's PRIMARY KEY ON CONFLICT IGNORE works
    data = {
        'ID'      : ['20230217093000A'],
        'Datetime': ['2023-02-17 09:30:00'],
        'Symbol'  : ['A'],
        'Close'   : ['147.014999389648'], 
        'High'    : ['147.270004272461'],
        'Low'     : ['146.919998168945'], 
        'Open'    : ['147.259994506836'], 
        'Volume'  : ['39644.0'],
    }
    df = pd.DataFrame(data)
    df = df.set_index('ID')
    df.to_sql('prices', db_connection, if_exists='append', index=True, index_label='ID')               
    df.to_sql('prices', db_connection, if_exists='append', index=True, index_label='ID')               
    # Read thesaved data, shoul donly have one line
    query = "SELECT * FROM prices"
    new_df = pd.read_sql_query(query, db_connection)
    assert len(new_df) == 1
    # Close and delete our test DB
    db_connection.close()
    if os.path.isfile(test_file):
        os.remove(test_file)
