
import matplotlib.pyplot as plt
import numpy as np

x = [0, 3000, 6000]
y = [0, 4000, 0]

def draw(x, y, n):
    x_list = np.zeros((n, ))
    y_list = np.zeros((n, ))

    for i in range(3):
        x_list[i] = x[i]
        y_list[i] = y[i]

    x_0 = 3
    y_0 = 0
    for i in range(n -3):
        index = np.random.randint(0, 4)
        x_list[i+3] = int((x_list[index] + x_0) / 2)
        y_list[i+3] = int((y_list[index] + y_0) / 2)
        x_0 = x_list[i+3]
        y_0 = y_list[i+3]

    return x_list, y_list

x, y = draw(x, y, 10000000)
plt.scatter(x, y, color="k",s=0.5)
plt.show()