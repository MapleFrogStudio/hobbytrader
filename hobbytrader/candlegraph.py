# https://stackoverflow.com/questions/49684811/display-matplotlib-graph-in-browser
# https://www.geeksforgeeks.org/how-to-create-a-candlestick-chart-in-matplotlib/

# Change Cursor when over a region: https://matplotlib.org/stable/gallery/widgets/mouse_cursor.html

import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.widgets import Cursor
from hobbytrader.universe import TradeUniverse

class CandlesForDesktop:
    def __init__(self, stock_prices):
        self.data = stock_prices
        #self.fig, self.ax = plt.subplots(figsize=(12, 5) )
        self.fig = plt.figure(figsize=plt.figaspect(1/3), layout='constrained')
        self.ax = self.fig.add_subplot()

        # Style setup for candles chart
        self.color_up = 'green'
        self.color_down = 'red'
        self.data['Color'] = self.color_down
        self.data.loc[self.data.Close > self.data.Open, 'Color'] = self.color_up        
        self.body_width = .5
        self.wick_width = .05
        self.show_candles()

        self.show_OHCL_values()
        self.add_cursor()
        self.clicked = 0

        self.setup_event_handers()

    def show_candles(self):
        self.ax.grid(color='whitesmoke', linestyle='-', linewidth=0.5, zorder=1)
        self.bodies = self.ax.bar(self.data.index, self.data.Close - self.data.Open, self.body_width, bottom=self.data.Open, color=self.data.Color, zorder=3) 
        self.wicks = self.ax.bar (self.data.index, self.data.High - self.data.Low, self.wick_width,  bottom=self.data.Low, color='black', zorder=2)         
        plt.xticks(rotation=30, ha='right')     
    
    def show_OHCL_values(self):
        i = self.data.index[-1]
        ohcl_str = f'i:{i} | O{stock_prices.Open[i]:.2f} H{stock_prices.High[i]:.2f} L{stock_prices.Low[i]:.2f} C{stock_prices.Close[i]:.2f}'
        self.ohcl_values = self.ax.text(0.2, 0.95, ohcl_str, transform=self.ax.transAxes)
        self.ohcl_values.set_visible(True)
        
    def setup_event_handers(self):    
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_over_chart)     
        self.fig.canvas.mpl_connect('button_press_event', self.graph_clicked)

    def on_mouse_move_over_chart(self, event):
        x, y = event.xdata, event.ydata
        if event.inaxes:
            i = min(int(x), self.data.index[-1])
            i = max(i, self.data.index[0])
            ohcl_str = f'i:{i} | O{stock_prices.Open[i]:.2f} H{stock_prices.High[i]:.2f} L{stock_prices.Low[i]:.2f} C{stock_prices.Close[i]:.2f}'
            self.ohcl_values.set_text(ohcl_str)
            print(f'IN  -> data coords {x} {y}, pixel coords {event.x} {event.y}, index:{i}')
        else:
            print(f'OUT -> data coords {x} {y}, pixel coords {event.x} {event.y}')

        if self.ax.stale:
            self.ax.figure.canvas.draw_idle()


    def add_cursor(self):
        self.cursor = Cursor(self.ax, horizOn=True, vertOn=True, useblit=True, color='yellow', linewidth = 1)


    def motion_hover(self, event):
        if event.inaxes == self.ax:
            for bar in self.bodies:
                is_contained, annotation_index = bar.contains(event)
                if is_contained:
                    i = int(bar.get_x()) + 1
                    print(stock_prices.loc[[i]])
                    price_str = f'O:{stock_prices.Open[i]:.2f} H:{stock_prices.High[i]:.2f} L:{stock_prices.Low[i]:.2f} C:{stock_prices.Close[i]:.2f}'
                    self.somewhere.set_text(f'{price_str}')
                    if self.ax.stale:
                        self.fig.canvas.draw_idle() 
            

    def graph_clicked(self, event):
        if event.button == 3:
            self.annot.set_text(f'Right Button pressed: {self.clicked}')
            print('Right Button pressed...')
        if event.button == 1:
            self.annot.set_text(f'Left Button pressed: {self.clicked}')          
            print('Left Button pressed...')
        if event.button == 2:
            self.annot.set_text(f'Middle Button pressed: {self.clicked}')
            print('Middle button pressed')
        
        self.clicked += 1
        if self.ax.stale:
            self.fig.canvas.draw_idle()  



    # def add_annotation(self):
    #     self.annot = self.ax.annotate(text='Annotation', xy=(65825,212 ), transform=self.ax.transAxes, zorder=10)
    #     print('Add an annotation')

    # def add_cursor(self):
    #     #self.cursor = Cursor(self.ax, horizOn=True, vertOn=True, useblit=True, color='yellow', linewidth = 1)
    #     self.cursor = Cursor1(self.ax)

    # def add_text_somewhere(self):
    #     self.somewhere = self.ax.text(x=0.2, y=0.95, s='Somewhere', transform=self.ax.transAxes, zorder=10)
    #     print('Add some text somewhere...')

    def show(self):
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
    #g.add_cursor()
    g.show()
  
