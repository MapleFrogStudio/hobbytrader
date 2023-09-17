import msvcrt
from hobbytrader.database import load_OHLCV_from_db_for_symbols

class ConsolePrinter:
    def __init__(self, symbol_to_print, stock_data):
        self.ticker = symbol_to_print
        self.ohclv_data = stock_data[stock_data.Symbol == symbol_to_print]
        self.total_rows = len(stock_data)
        self.current_index = 0
        self.dates = self.ohclv_data.Datetime.values.tolist()
        self.dates.sort()

    def next_date(self):
        if self.current_index + 1 < self.total_rows:
            self.current_index += 1
            return True
        else:
            return False

    def row_values(self):
        date_str = self.dates[self.current_index]
        row_data = self.ohclv_data[self.ohclv_data.Datetime == date_str]
        return row_data

    def print_header(self):
        header = f"{'Date':>19} | {'Open':>12} | {'High':>12} | {'Low':>12} | {'Close':>12} | {'Volume':>15} | "
        print(header)

    def print_row(self):
        #print(f'Current index: {self.current_index}')
        row_data = self.row_values()
        row_str = f'{row_data.Datetime.iloc[0]:>19} | '
        row_str +=f'{row_data.Open.iloc[0]:>12.2f} | '
        row_str +=f'{row_data.High.iloc[0]:>12.2f} | '
        row_str +=f'{row_data.Low.iloc[0]:>12.2f} | '
        row_str +=f'{row_data.Close.iloc[0]:>12.2f} | '
        row_str +=f'{row_data.Volume.iloc[0]:>15.0f} | '
        print(row_str)

    def grab_keyboard_input(self):
        key = msvcrt.getch().decode('utf-8').lower()                # pragma: no cover
        return key                                                  # pragma: no cover
    
    def print_interactive(self, start_index = None):
        if start_index is not None:                                 # pragma: no cover
            if start_index < self.total_rows and start_index >= 0:  # pragma: no cover
                self.current_index = start_index                    # pragma: no cover
        
        print('CTRL-C to quit, ENTER to display next row')          # pragma: no cover
        self.print_header()                                         # pragma: no cover
        self.print_row()                                            # pragma: no cover
        while self.next_date():                                     # pragma: no cover
            self.grab_keyboard_input()                              # pragma: no cover
            self.print_row()                                        # pragma: no cover
