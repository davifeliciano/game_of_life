import argparse
import concurrent.futures
import numpy as np
from numpy.random import default_rng
import matplotlib.pyplot as plt

from gameoflife import GameOfLife
from timing import timer

parser = argparse.ArgumentParser(
    description='Plot the evolution of a given number of games of life over a given number of generations'
)

parser.add_argument('height', type=int, help='the height of the game')
parser.add_argument('width', type=int, help='the width of the game')

parser.add_argument('-n', type=int, nargs='?', default=10, const=10,
                    help='the number of games in the plot')

parser.add_argument('-g', type=int, nargs='?', default=20, const=20,
                    help='the number of generations of each game in the plot')

parser.add_argument('-t', '--type', type=str, nargs='?', default='moore', const='moore',
                    help='the type of the games. could be \'moore\' or \'vonneumann\'')

parser.add_argument('-o', '--order', type=int, nargs='?', default=1, const=1,
                    help='the order of the neighborhood to be considered in the calculations')

parser.add_argument('-e', '--elite', type=float, nargs='?', default=0., const=0.,
                    help='the proportion of the alive individuals that will be randomly promoted to immortals')

parser.add_argument('-x', '--expec', type=int, nargs='?', default=5, const=5,
                    help='after this number of generations the immortals will be randomly chosen again')

parser.add_argument('-f', '--file', type=str, nargs='?', default='plot.png', const='plot.png',
                    help='name of the output file. default is plot.png')

args = parser.parse_args()

n = args.n
gens = args.g
shape = args.height, args.width
ntype = args.type
norder = args.order
elite = args.elite
expec = args.expec
filename = args.file

rng = default_rng()


def main():

    series = np.ndarray(shape=(n, gens), dtype=int)
    games = []

    for i in range(n):
        state = rng.choice([0, 1], size=shape)
        games.append(GameOfLife(state, norder, ntype, elite, expec))

    for gen in range(gens):
        print(f'Computing generation {gen + 1} of {gens}')
        for i in range(n):
            series[i][gen] = games[i].count_alive()
            games[i].update()

    print('Ploting series')

    fig, ax = plt.subplots()

    ax.set(xlim=(1, gens),
           xticks=range(1, gens + 1),
           )

    t = np.arange(1, gens + 1)

    for i in range(n):
        ax.plot(t, series[i])

    print(f'Saving image on {filename}')

    plt.savefig(filename, dpi=300)


if __name__ == '__main__':
    main()
