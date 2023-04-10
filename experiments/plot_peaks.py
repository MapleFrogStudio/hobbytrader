import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


tsla = yf.download('TSLA',period='1y')
x = tsla.index
y = tsla.Close.to_list()

print(x)
print(y)

#x = np.linspace(0,10, 100)
#y = x * np.random.randn(100)**2

# Find maximas of the function
peaks_i = find_peaks(y)
peaks = find_peaks(y, height=1, threshold=1, distance=1)
heights = peaks[1]['peak_heights']      # Height of out peaks
peak_pos = x[peaks[0]]                  # Liste of the peaks on x axis



#print(peaks_i)
#print(peaks)
#print(heights)

fig = plt.figure()
ax = fig.subplots()
ax.plot(x,y)
ax.scatter(peak_pos, heights, color='r', s=15, marker='D', label='Maximuma')
ax.legend()
ax.grid()
plt.show()