# script for generate kasago-pattern
# 30　Aug 2022 @tama_Ud

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as plcolors


def generate_grid_figure():  # generate 100x100 grid figure with binary colors
    # TODO: check which is upper val
    cmap = plcolors.ListedColormap(['white', 'black'])  # 0,1
    rcshape = np.reshape(np.random.rand(10000), newshape=(100, 100))
    im = plt.imshow(rcshape,
                    cmap=cmap,
                    interpolation='none',
                    vmin=0, vmax=1,
                    aspect='equal')

    ax = plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])

    #print(get_color((0, 0), rcshape))
    #print(get_color((0, -1), rcshape))

    plt.show()


# ref. https://matplotlib.org/stable/tutorials/intermediate/imshow_extent.html#sphx-glr-tutorials-intermediate-imshow-extent-py
def get_color(data, idx):
    """Return the data color of an index."""
    threshold, upper, lower = 0.5, 1, 0
    val = data[idx] / data.max()  # normalize 0 to 1
    return np.where(val > threshold, upper, lower)  # binarize 0 or 1


# def get_moore_neighborhood_cell_states(data, index, weight=1):
#     # rx, ry = relative coordinate from 0,0
#     # [-1,1], [0,1], [1,1] -> y is always 1
#     # [-1,0], [0,0], [1,0] -> y is always 0
#     # [-1,-1], [0,-1], [1,-1] -> y is always -1

#     sum = 0
#     rcood = [-1, 0, 1]
#     for ry in rcood:
#         for rx in rcood:
#             rindex = np.sum(index, [rx, ry])
#             sum += get_color(data, rindex)
#     return sum*weight


def get_around_moore_cell_states(data, index, distance, mweight=1, aweight=-0.4):
    # rx, ry = relative coordinate from [0,0] (distance=3)
    # moore neighborhood = ([rx, ry] = -1 to 1)
    # [-3,3] ... [3,3] -> y is always 3
    # ...
    # [-3,0] ... [3,0] -> y is always 0
    # ...
    # [-3,-3] ... [3,-3] -> y is always -3

    msum = 0
    asum = 0
    for ry in range(-distance, distance+1):
        for rx in range(-distance, distance+1):

            if -1 <= rx & ry <= 1:
                msum += get_color(data, rindex)
                continue

            rindex = np.sum(index, [rx, ry])
            asum += get_color(data, rindex)
    return msum*mweight + asum*aweight


if __name__ == "__main__":
    generate_grid_figure()

# DONE: check around cell state
# MEMO: np.shape index is not equal to plt index
# TODO: calculate cell weight
# TODO: define cell dead or alive
# TODO: imshow
