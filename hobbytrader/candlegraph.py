# https://stackoverflow.com/questions/49684811/display-matplotlib-graph-in-browser
# https://www.geeksforgeeks.org/how-to-create-a-candlestick-chart-in-matplotlib/

import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.widgets import Cursor

from hobbytrader.universe import TradeUniverse


class CandlesForDesktop:
    def __init__(self, stock_prices):
        self.data = stock_prices
        self.fig, self.ax = plt.subplots()

        # Style setup for candles chart
        self.color_up = 'green'
        self.color_down = 'red'
        self.data['Color'] = self.color_down
        self.data.loc[self.data.Close > self.data.Open, 'Color'] = self.color_up        
        self.body_width = .5
        self.wick_width = .05
        self.add_candles()

        # Setup prices display
        self.prices_display_text = 'Test'
        self.prices_display_xy = self.calc_annotation_position()
        self.prices_annotation = self.ax.annotate(
            text= self.prices_display_text,
            #xy = annotation_position,
            xy  = self.prices_display_xy
        )

    def add_candles(self):
        self.ax.grid(color='whitesmoke', linestyle='-', linewidth=0.5, zorder=1)
        self.bodies = self.ax.bar(self.data.index, self.data.Close - self.data.Open, self.body_width, bottom=self.data.Open, color=self.data.Color, zorder=3) 
        self.wicks = self.ax.bar (self.data.index, self.data.High - self.data.Low, self.wick_width,  bottom=self.data.Low, color='black', zorder=2)         
        plt.xticks(rotation=30, ha='right')     

    def calc_annotation_position(self, offset_percentage_from_top=0.05, offset_percentage_from_left=0.05):
        y_limits = self.ax.get_ylim()
        height = y_limits[1] - y_limits[0]
        offset_from_top = y_limits[1] - (height * offset_percentage_from_top)
        
        x_limits = self.ax.get_xlim()
        width = x_limits[1] - x_limits[0]
        offset_from_left = x_limits[0] + (width * offset_percentage_from_left)

        return offset_from_left, offset_from_top
    
    def setup_event_handers(self):
        self.fig.canvas.mpl_connect('motion_notify_event', self.motion_hover)
        #self.ax.callbacks.connect('xlim_changed', self.update_prices_position)
        #self.ax.callbacks.connect('ylim_changed', self.motion_hover)        
        #fig.canvas.mpl_connect('button_press_event', motion_hover)

    def motion_hover(self, event):
        if event.inaxes == self.ax:
            for bar in self.bodies:
                is_contained, annotation_index = bar.contains(event)
                if is_contained:
                    i = int(bar.get_x()) + 1
                    print(stock_prices.loc[[i]])


    def add_cursor(self):
        self.cursor = Cursor(self.ax, horizOn=True, vertOn=True, useblit=True, color='yellow', linewidth = 1)

    def plot(self):
        plt.show() 


if __name__ == '__main__':
    symbols = ['TSLA']
    u = TradeUniverse(symbols)
    u.load_universe_data_all_dates()
    tmp_df = u.datas.sort_values(by='Datetime')

    stock_prices = tmp_df[-150:].copy()
    #stock_prices['Datetime'] = pd.to_datetime(stock_prices['Datetime'])
    stock_prices.reset_index(drop=True)
    print(stock_prices)

    g = CandlesForDesktop(stock_prices)
    g.add_cursor()
    g.plot()
  
