import sys
import pandas as pd
import sqlite3

DBPATH = 'DB/minute.sqlite'

def execute_sql(sql):
    conn = sqlite3.connect(DBPATH)
    data = pd.read_sql_query(sql, conn, coerce_float=True, parse_dates=['Datetime'])
    conn.close()    

    return data

def read_filter(symbol='GEVO', datestr='2023-05-01'):
    sql = f"""
        SELECT * FROM prices
        WHERE Symbol = '{symbol}'
        AND date(Datetime) = '{datestr}'
    """
    data = execute_sql(sql)
    
    return data


if __name__ == '__main__':
    print('Working....')
    data_1m = read_filter('AMD', '2023-05-01')
    data_1m.set_index(['Datetime'], inplace=True)
    data_1m = data_1m[['Symbol','Open','High','Low','Close','Volume']]
    print(data_1m.head(11))
    print(data_1m.index.name)
    data_10m = data_1m.resample('10T', origin='start').agg({'Symbol':'first','Open':'first','High':'max','Low':'min','Close':'last','Volume': 'sum'})
    print(data_10m.head(5))


