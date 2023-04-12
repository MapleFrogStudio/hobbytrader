import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np

linear = [x for x in range(5)]
square = [x**2 for x in linear]
cube   = [x**3 for x in linear]


def plot_01():
    plt.subplot(3, 1, 1)
    plt.plot(linear)

    plt.subplot(3, 1, 2)
    plt.plot(square)

    plt.subplot(3, 1, 3)
    plt.plot(cube)

    print(linear)
    print(square)
    print(cube)

    #plt.tight_layout()
    plt.show()


def plot_02():
    plt.subplot(3, 1, 1)
    plt.plot(linear)
    plt.xticks(alpha=0)

    plt.subplot(3, 1, 2)
    plt.plot(square)
    plt.xticks(alpha=0)

    plt.subplot(3, 1, 3)
    plt.plot(cube)

    print(linear)
    print(square)
    print(cube)

    plt.suptitle('Demo triple plot')
    #plt.tight_layout()
    plt.show()    

# plot_01()
plot_02()