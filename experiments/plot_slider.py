import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider 

# Initial function
x = np.linspace(0, 10, 30)
y = np.sin(0.5 * x) * np.sin(x * np.random.randn(30))
#Spline interpolatyion
spline = UnivariateSpline(x, y, s=6)
x_spline = np.linspace(0, 10, 1000)
y_spline = spline(x_spline)
# Plotting
fig = plt.figure()
ax = fig.subplots()
p1 = ax.plot(x, y)
p2, = ax.plot(x_spline, y_spline, color='green')
# Slider - make some space for slider
plt.subplots_adjust(bottom = 0.25)
# Define the slider area and it'S configuration and connect to graph
ax_slide = plt.axes([0.25, 0.1, 0.65, 0.03])    # x,y, width, height
s_factor = Slider(ax_slide, 'Smoothing', valmin=0.1, valmax=6, valinit=6, valstep=0.2) # Target axes, Lable, min val, max val, initial value, step

def update(slider_val):
    current_value = s_factor.val
    spline = UnivariateSpline(x, y, s=current_value)
    p2.set_ydata(spline(x_spline))
    fig.canvas.draw()   # Redraw the figure only

s_factor.on_changed(update) # s_factor calue is passed by default to update

plt.show()