# script for generate kasago-pattern
# 30　Aug 2022 @tama_Ud

from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as plcolors
import asyncio

N = 100  # grid scale
cmap = plcolors.ListedColormap(['white', 'black'])  # 0,1


def generate_grid_shape(scale=N):
    # generate 100x100 grid shape with binary colors
    return np.reshape(np.random.rand(scale**2), newshape=(scale, scale))


def show_figure(data):
    im = plt.imshow(data,
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


def get_around_moore_cell_states(data, index, distance=3, mweight=1, aweight=-0.4):
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

            rindex = np.sum([index, [rx, ry]])
            asum += get_color(data, rindex)  # TODO: debug return np array
    return msum*mweight + asum*aweight


def calculate_dead_or_alive(data, index, state, threshold=0):
    if threshold <= state:
        # draw black (alive)
        data[index] = 1
    else:
        #  draw white (dead)
        data[index] = 0


async def main():
    data = deepcopy(generate_grid_shape())
    show_figure(deepcopy(data))

    for _ in range(4):
        for i in range(N):
            for j in range(N):
                state = get_around_moore_cell_states(deepcopy(data), [i, j])
                calculate_dead_or_alive(deepcopy(data), [i, j], state)
            print(i + " loop now!")
        show_figure(deepcopy(data))
        await asyncio.sleep(0.1)
        # TODO: check data is copied instance?
    print("calculate done!")


if __name__ == "__main__":
    asyncio.run(main())
