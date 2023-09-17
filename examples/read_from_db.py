import sys
import pandas as pd
import sqlite3

DBPATH = 'DB/minute.sqlite'

def show_help():
    print(f'\nSimulator options')
    print(f'    1: Get prices for symbol="GEVO"')
    print(f'    2: Get prices for Date&time 2023-05-01 09:31:00')
    print(f'    3: Get prices for Date 2023-05-01')
    print(f'    4: Get prices filtered for symbol="GEVO", datestr="2023-05-01"')


def execute_sql(sql):
    conn = sqlite3.connect(DBPATH)
    data = pd.read_sql_query(sql, conn, coerce_float=True, parse_dates=['Datetime'])
    conn.close()    

    return data

def read_symbol(symbol='GEVO'):
    sql = f"""
        SELECT * FROM prices
        WHERE symbol = '{symbol}'
    """
    data = execute_sql(sql)
    return data

def read_datetime(datetimestr='2023-05-01 09:31:00'):
    sql = f"""
        SELECT * FROM prices
        WHERE Datetime = '{datetimestr}'
    """
    data = execute_sql(sql)
    
    return data

def read_date(datestr='2023-05-01'):
    sql = f"""
        SELECT * FROM prices
        WHERE date(Datetime) = '{datestr}'
    """
    data = execute_sql(sql)
    
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

    if len(sys.argv) <= 1:
        show_help()
        quit()

    if sys.argv[1] == '1':
        data_df = read_symbol('GEVO')
        print(data_df)
        quit()

    if sys.argv[1] == '2':
        data_df = read_datetime('2023-05-01 09:31:00')
        print(data_df)
        quit()

    if sys.argv[1] == '3':
        data_df = read_date('2023-05-01')
        print(data_df)
        quit()

    if sys.argv[1] == '4':
        data_df = read_filter('GEVO', '2023-05-01')
        print(data_df)
        quit()

    if sys.argv[1] not in ['1','2','3','4']:
        # We assume it is a symbol
        symbol = sys.argv[1]
        data_df = read_symbol(symbol=symbol)
        print(data_df)
        quit()