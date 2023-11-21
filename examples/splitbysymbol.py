import sqlite3
import json
from hobbytrader.database import open_sqlite_db, load_OHLCV_from_db_for_symbols, save_to_sqlite

source_db = 'DB\minute.sqlite'

# Connect to the SQLite database
conn = sqlite3.connect(source_db)
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT Symbol FROM prices")
symbols = [row[0] for row in cursor.fetchall()]

# Close the cursor and connection
cursor.close()
conn.close()

# 'symbols' now contains all unique symbols from the table
#print(symbols)
json_data = {"symbols": symbols}
json_output = json.dumps(json_data)

print(json_output)

# for symbol in symbols:
#     slist = [symbol]
#     data_df = load_OHLCV_from_db_for_symbols(source_db, slist)
#     save_to_sqlite(f'DB/DB/2023-{symbol}.sqlite', data_df)
