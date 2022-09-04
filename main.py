# script for generate kasago-pattern
# 30　Aug 2022 @tama_Ud

from typing import Any
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as plcolors
import asyncio

N = 100  # grid scale
data = np.reshape(np.random.rand(N**2), newshape=(N, N))
cmap = plcolors.ListedColormap(['white', 'black'])  # 0,1


def generate_grid_shape():
    # generate NxN grid shape with binary colors
    # data = np.reshape(np.random.rand(scale**2), newshape=(scale, scale))

    print("data address 1", id(data))

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
def get_color(idxarr):
    """Return the data color of an index."""
    threshold, upper, lower = 0.5, 1, 0
    # TODO: fix IndexError: index 100 is out of bounds for axis 1 with size 100
    val = data[idxarr[0], idxarr[1]] / data.max()  # normalize 0 to 1
    print("idxarr", idxarr)
    #print("data[idxarr]", data[idxarr])
    print("data.max()", data.max())
    print("color:", np.where(val > threshold, upper, lower))
    return np.where(val > threshold, upper, lower).item()  # binarize 0 or 1


def get_around_moore_cell_states(index, distance=3, mweight=1, aweight=-0.4):
    # rx, ry = relative coordinate from [0,0] (distance=3)
    # moore neighborhood = ([rx, ry] = -1 to 1)
    # [-3,3] ... [3,3] -> y is always 3
    # ...
    # [-3,0] ... [3,0] -> y is always 0
    # ...
    # [-3,-3] ... [3,-3] -> y is always -3

    print("data address 2", id(data))

    msum = 0
    asum = 0
    for ry in range(-distance, distance+1):
        # skip if ry is over 100
        if ry > 100:  # TODO: refactor to inline args
            continue

        for rx in range(-distance, distance+1):
            # skip if rx or ry is over 100
            if rx > 100:  # TODO: refactor to inline args
                continue

            # skip moore neighborhood
            if -1 <= rx & ry <= 1:
                msum += get_color(index)
                continue

            rindex = np.sum([index, [rx, ry]], axis=0)
            asum += get_color(rindex)
    return (msum*mweight + asum*aweight)


def calculate_dead_or_alive(index, state, threshold=0.0):

    # threshold = float
    # state = np.ndarray

    if threshold <= state:
        # draw black (alive)
        data[index] = 1
    else:
        #  draw white (dead)
        data[index] = 0


async def main():
    generate_grid_shape()
    print("data address 1", id(data))

    for _ in range(4):
        for i in range(N):
            for j in range(N):
                state = get_around_moore_cell_states([i, j])  # np.array
                calculate_dead_or_alive([i, j], state)
            print(i + " loop now!")
        plt.imshow(data,
                   cmap=cmap,
                   interpolation='none',
                   vmin=0, vmax=1,
                   aspect='equal')
        plt.show()
        await asyncio.sleep(0.1)
    print("calculate done!")


if __name__ == "__main__":
    asyncio.run(main())
