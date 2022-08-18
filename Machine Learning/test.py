import matplotlib.pyplot as plt
import numpy as np


mass = 1.9891e30
radius = (1391016*1000)/2

def gravity(x, y, mass, radius):
	G = 6.674e-11
	g = np.where((x**2+y**2)**(1/2) >= radius, G*mass/(x**2+y**2),0)
	return g

x = y = np.linspace(-1_000_000_000 - radius, 1_000_000_000 + radius, 10000)
X, Y = np.meshgrid(x, y)

Z = gravity(X, Y, mass, radius)

fig = plt.figure()
graph = plt.contourf(X, Y, Z)
fig.colorbar(graph)
plt.show()
