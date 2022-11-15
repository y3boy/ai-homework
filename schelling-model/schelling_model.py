import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange
from typing import List
from random import randint

N = 20                  # size of array
SIZE = N * N
SWAPS = pow(10, 6)    # amount of swaps cells

HAPPY_RATION = 2        # number of neighbors to be happy
OCCUPIED_RATION = 0.45  # occupied in percentages (separate for BLUE & RED)
VACANT_RATION = 0.1     # vacant places 

SCATTER_SIZE = N/10 * 2 # size of scatter

BLUE, RED, WHITE = 0, 1, -1 # value of colors
VACANT = WHITE


def pltcolor(arr: List) -> List:
    """Return list of point colors"""
    colors_set = {BLUE: 'blue', RED: 'red', VACANT: 'white'}
    colors = list()
    for item in arr:
        colors.append(colors_set.get(item))
    return colors


@njit
def relocation(arr: List):
    """Relocation """
    matrix = np.reshape(arr, (N, N))
    vacant = [[id//N, id%N] for id, value in enumerate(arr) if value == VACANT]
    for i in prange(SWAPS):
        index = randint(0, N-1)
        y = index // 10
        x = index % 10
        if matrix[y][x] != VACANT:
            neighbors = list()
            if y == 0:
                if x == 0:
                    neighbors.extend([matrix[y][x+1], matrix[y+1][x], matrix[y+1][x+1]])
                elif x == N-1:
                    neighbors.extend([matrix[y][x-1], matrix[y+1][x], matrix[y+1][x-1]])
                else:
                    neighbors.extend([matrix[y+1][x-1], matrix[y+1][x], matrix[y+1][x+1],
                                      matrix[y][x-1], matrix[y][x+1]])
            elif y == N-1:
                if x == 0:
                    neighbors.extend([matrix[y][x+1], matrix[y-1][x], matrix[y-1][x+1]])
                elif x == N-1:
                    neighbors.extend([matrix[y][x-1], matrix[y-1][x], matrix[y-1][x-1]])
                else:
                    neighbors.extend([matrix[y-1][x-1], matrix[y-1][x], matrix[y-1][x+1],
                                      matrix[y][x-1], matrix[y][x+1]])
            else:
                if x == 0:
                    neighbors.extend([matrix[y+1][x], matrix[y+1][x+1], matrix[y][x+1],
                                      matrix[y-1][x-1], matrix[y-1][x]])
                if x == N-1:
                    neighbors.extend([matrix[y+1][x], matrix[y+1][x-1], matrix[y][x-1],
                                      matrix[y-1][x-1], matrix[y-1][x]])
                else:
                    neighbors.extend([matrix[y+1][x+1], matrix[y+1][x], matrix[y+1][x-1],
                                      matrix[y-1][x+1], matrix[y-1][x], matrix[y-1][x-1],
                                      matrix[y][x+1], matrix[y][x-1]])
            
            if neighbors.count(matrix[y][x]) < HAPPY_RATION:
                index = randint(0, len(vacant)-1)
                vacant_y = vacant[index][0]
                vacant_x = vacant[index][1]
                
                arr[vacant_y*10 + vacant_x] = matrix[y][x]
                arr[y*10 + x] = VACANT
                
                matrix[vacant_y][vacant_x] = matrix[y][x]
                matrix[y][x] = VACANT

                vacant.pop(index)
                vacant.append([y, x])


def main():
    array = np.zeros(SIZE, dtype=np.int8)
    # Brilliant way to fill array
    array[:int(SIZE*OCCUPIED_RATION)] = 1
    array[-int(SIZE*VACANT_RATION):] = -1
    np.random.shuffle(array)

    ox = [i for i in range(N)] * N
    oy = [i//N for i in range(N*N)]

    fig, ax = plt.subplots()
    ax.scatter(x=ox, y=oy, marker='s', c=pltcolor(arr=array))

    ax.set_facecolor('black')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    fig.set_figwidth(SCATTER_SIZE) 
    fig.set_figheight(SCATTER_SIZE)
    ax.set_title('Created map')

    plt.show()

    relocation(arr=array)

    fig, ax = plt.subplots()
    ax.scatter(x=ox, y=oy, marker='s', c=pltcolor(arr=array))
    ax.set_facecolor('black')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    fig.set_figwidth(SCATTER_SIZE) 
    fig.set_figheight(SCATTER_SIZE)
    ax.set_title('After relocation map')

    plt.show()


if __name__ == '__main__':
    main()