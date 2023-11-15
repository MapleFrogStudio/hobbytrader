import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Cursor

class Chart1:
    def __init__(self):
        x = np.arange(0, 1, 0.01)
        y = np.sin(2 * 2 * np.pi * x)

        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Simple cursor')
        self.ax.plot(x, y, 'o')

        self.textin = self.ax.text(0.72, 0.9, 'Cursor Inside Axes', transform=self.ax.transAxes)
        self.textin.set_visible(False)
        self.textout = self.ax.text(0.02, 0.10, "Cursor Outside Axes", transform=self.ax.transAxes)
        self.textout.set_visible(False)

        self.add_cursor()
        self.add_event_handlers()


    def add_event_handlers(self):
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.fig.canvas.mpl_connect('figure_leave_event', self.on_leave_figure)

    def on_leave_figure(self, event):
        self.textin.set_visible(False)
        self.textout.set_visible(False)
        self.ax.figure.canvas.draw_idle()
        print(f'Leaving figure area...')

    def on_mouse_move(self, event):
        x, y = event.xdata, event.ydata
        if event.inaxes:
            self.textin.set_text(f'x:{x:.2}, y:{y:.2}')
            self.textin.set_visible(True)
            self.textout.set_visible(False)
            print(f'IN  -> data coords {x} {y}, pixel coords {event.x} {event.y}')
        else:
            print(f'OUT -> data coords {x} {y}, pixel coords {event.x} {event.y}')
            self.textin.set_visible(False)
            self.textout.set_visible(True)
            
        if self.ax.stale:
            self.ax.figure.canvas.draw_idle()

    def add_cursor(self):
        self.cursor = Cursor(self.ax, horizOn=True, vertOn=True, useblit=True, color='yellow', linewidth = 1)
        

if __name__ == '__main__':
    print(f'Matplotlib version: {matplotlib.__version__}')
    print(f'Backend used: {matplotlib.get_backend()}')
    c = Chart1()
    plt.show()