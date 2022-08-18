from lib.data_gen import Lorenz63
import matplotlib.pyplot as plt
import numpy as np


samples = 100

data = Lorenz63(size=7000, discard=5000)

for i in range(samples -1):

	new_data = Lorenz63(size=7000, discard=5000)

	data = np.concatenate((data, new_data))

np.savetxt("dataset.csv", data, delimiter=", ")

# val = np.loadtxt(r"C:\Users\daniel koval\Desktop\Luciano\Programación\Visual Studio\Machine Learning\val_pred.csv", delimiter=", ")

# plt.axes(projection="3d").plot(val[:, 0], val[:, 1], val[:, 2])
# plt.show()
