import matplotlib.pyplot as plt
import numpy as np

# Disable interactive mode to prevent the toolbar
plt.ioff()

x = np.arange(0, 1, 0.01)
y = np.sin(2 * 2 * np.pi * x)

# Create a figure and plot
fig, ax = plt.subplots(layout='constrained')
ax.set_title('Simple cursor')
ax.plot(x, y, 'o')

plt.show()

# Re-enable interactive mode (optional)
plt.ion()
