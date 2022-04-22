import numpy as np
import matplotlib.pyplot as plt

# should always be 15 (16 - 1)
A_div = 15
n_div = 15

A = np.linspace(0, -60, A_div)
n = np.linspace(2.5, 5.5, n_div)
Z = np.load('plot_npy/allfloor_div16_0.npy')

A, n = np.meshgrid(A, n)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel("A")
ax.set_ylabel("n")
ax.set_zlabel("Error (m)")
ax.plot_surface(A, n, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')

plt.show()
