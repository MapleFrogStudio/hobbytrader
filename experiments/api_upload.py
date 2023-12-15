import sys
import sqlite3
import requests
import json

from hobbytrader import database


source_db = f'DB/minute.sqlite'

# Connect to the SQLite database
conn = sqlite3.connect(source_db)
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT Symbol FROM prices")
symbols = [row[0] for row in cursor.fetchall()]

if len(sys.argv) <= 1:
    print("No ticker symbol provided...")
    quit()

symbol = sys.argv[1]
if symbol not in symbols:
    print("Symbol not found in DB...")
    quit()

cursor.execute(f"SELECT ID, Datetime, Symbol, Open, High, Low, Close, Volume FROM prices WHERE Symbol = ?", (symbol,))
prices = cursor.fetchall()

# Close the cursor and connection
cursor.close()
conn.close()

#print(symbols)
print('-------------------')
print(symbol)
print('-------------------')
print(prices[-1])
print('-------------------')
print(prices[-1][0])
print(prices[-1][1])
print(prices[-1][2])
print(prices[-1][3])
print(prices[-1][4])
print(prices[-1][5])
print(prices[-1][6])
print(prices[-1][7])

print('----- DEMO POST -----')
for price in prices:
    # Define new data to create
    price_to_add = {
        "datetime": price[1],
        "symbol"  : price[2],
        "open"    : price[3],
        "high"    : price[4],
        "low"     : price[5],
        "close"   : price[6],
        "volume"  : price[7],
        "apikey"  : 'hvB4RR1NxsTjk2A2b3Z84HzBgUMSOR2JajFodJCQv1lvGqlH28'
    }
    url_post = "https://api.maplefrogstudio.com/symbols"
    post_response = requests.post(url_post, data=price_to_add, timeout=10)

    # Print the response
    print(post_response.status_code)
    if post_response.status_code == 201:
        post_response_json = post_response.json()
        print(post_response_json)