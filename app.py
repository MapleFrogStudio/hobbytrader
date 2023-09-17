import json
from hobbytrader import database
from hobbytrader.trades import Trades
from hobbytrader.universe2 import TradeUniverse
from datetime import datetime

if __name__ == '__main__':
    db_path = 'DB/minute.sqlite'
    symbols = ['TSLA', 'AAPL', 'GIB-A.TO']
    
    u = TradeUniverse(symbols, load_data=True, db_path=db_path)
    print(f'Symbols: {symbols}')
    print(f'Number of datas record: {len(u.datas)}')
    index = 2
    print(f"Check for {symbols[index]} presence\n {u.datas.query('Symbol == @symbols[@index]').head(5)}")
    print('-----')
    # print(f'Number of dates: {len(u.dates)}, [1600:1610]')
    # print(u.dates[1600:1610])
    # print('-----')
    # for dt in u.dates[1600:]:
    #     df = u.prices_for_date(dt)
    #     print(f'Current date: {u.date}')
    #     print(df)
    #     print('------')
    #     input('ENTER next / CTRL-C Quit')

    u.date_index = 1000
    while True:
        print(f'Current date: {u.date}')
        print(u.prices_for_date(u.date))
        user_input = input('ENTER - Next date, CTRL-C Quit')
        if not u.next_dt():
            break

