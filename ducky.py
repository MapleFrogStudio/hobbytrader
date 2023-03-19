import duckdb
cursor = duckdb.connect('tsx.duckdb')
data = duckdb.read_csv('DATASET/SP500-2023-03-19.csv')
#query = "SELECT * FROM read_csv_auto('DATASET/SP500-2023-03-19.csv');"
#results = cursor.execute(query)
print(data)
