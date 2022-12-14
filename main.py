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

    im = plt.imshow(data,
                    cmap=cmap,
                    interpolation='none',
                    vmin=0, vmax=1,
                    aspect='equal')

    ax = plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()


# ref. https://matplotlib.org/stable/tutorials/intermediate/imshow_extent.html#sphx-glr-tutorials-intermediate-imshow-extent-py
def get_color(idxarr):
    """Return the data color of an index."""
    threshold, upper, lower = 0.5, 1, 0
    # normalize 0 to 1
    # TODO: fix error? invalid value encountered in double_scalars
    # TODO: 1回目の計算の後、画面が真っ黒になる -> 白に変更できているか確認 -> 色変更関数 -> セルの指定関数
    val = data[idxarr[0], idxarr[1]] / data.max()
    return np.where(val > threshold, upper, lower).item()  # binarize 0 or 1


def get_around_moore_cell_states(indexarr, distance=3, mweight=1, aweight=-0.2):
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

            # skip moore neighborhood
            if -1 <= rx & rx <= 1:
                if -1 <= ry & ry <= 1:
                    msum += get_color(indexarr)
                    continue

            rindex = [np.sum(rx + indexarr[0]), np.sum(ry + indexarr[1])]

            # skip if ry is over 100
            if N-1 < rindex[0] or rindex[0] < 0:  # TODO: refactor to inline args
                continue

            # skip if rx is over 100
            if N-1 < rindex[1] or rindex[1] < 0:  # TODO: refactor to inline args
                continue

            # print("rindex", rindex)
            asum += get_color(rindex)
    #print("msum*mweight", msum*mweight)
    #print("asum*aweight", asum*aweight)
    return (msum*mweight + asum*aweight)


def calculate_dead_or_alive(state, threshold=0.0):

    # threshold = float
    # state = np.ndarray

    if threshold <= state:
        # draw black (alive)
        return 1
    else:
        #  draw white (dead)
        return 0


async def main():
    generate_grid_shape()
    # calculate cell dead or alive 4 times
    for _ in range(8):
        for i in range(0, N, 6):
            for j in range(N):
                state = get_around_moore_cell_states([i, j])  # np.array
                data[i, j] = calculate_dead_or_alive(data[i, j], state)
    # うまく表示されない...
    plt.imshow(data,
               cmap=cmap,
               interpolation='none',
               vmin=0, vmax=1,
               aspect='equal')
    plt.show()

if __name__ == "__main__":
    asyncio.run(main())
