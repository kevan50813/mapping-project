import numpy as np
import matplotlib.pyplot as plt

# should always be 15 (16 - 1)
A_div = 15
n_div = 15

#A = np.linspace(64, -64, A_div)
#n = np.linspace(2, 8, n_div)

A = np.linspace(37, 17, A_div)
n = np.linspace(6.5, 8.5, n_div)

Z = np.load('plot_npy/floor4_div16_2.npy')

A, n = np.meshgrid(A, n)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel("A")
ax.set_ylabel("n")
ax.set_zlabel("Error (m)")
ax.plot_surface(A, n, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
ax.view_init(20, 60)

plt.show()
