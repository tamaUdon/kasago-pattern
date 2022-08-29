import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as plcolors

# generate 100x100 grid figure with binary colors
cmap = plcolors.ListedColormap(['black', 'white'])
im = plt.imshow(np.reshape(np.random.rand(10000), newshape=(100, 100)),
                cmap=cmap,
                interpolation='none',
                vmin=0, vmax=1,
                aspect='equal')

ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])

plt.show()

# TODO: check around cell state
# TODO: calculate cell weight
# TODO: define cell dead or alive
