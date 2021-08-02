import argparse
import numpy as np
from numpy.random import default_rng
import matplotlib.pyplot as plt

from gameoflife import GameOfLife

parser = argparse.ArgumentParser(
    description='plot the evolution of a given number of Conways Games of Life over a given number of generations',
    epilog='the final plot will contain the average of the population with and without an elite, for comparisson purposes'
)

parser.add_argument('height', type=int, help='the height of the game')
parser.add_argument('width', type=int, help='the width of the game')

parser.add_argument('-n', type=int, nargs='?', default=10, const=10,
                    help='the number of games in the plot')

parser.add_argument('-g', type=int, nargs='?', default=20, const=20,
                    help='the number of generations of each game in the plot')

parser.add_argument('-t', '--type', type=str, nargs='?', default='moore', const='moore',
                    help='the type of the games. Could be \'moore\' or \'vonneumann\'')

parser.add_argument('-o', '--order', type=int, nargs='?', default=1, const=1,
                    help='the order of the neighborhood to be considered in the calculations')

parser.add_argument('-e', '--elite', type=float, nargs='?', default=0.05, const=0.05,
                    help='the proportion of the alive individuals that will be randomly promoted to immortals. The default values is 5')

parser.add_argument('-x', '--expec', type=int, nargs='?', default=5, const=5,
                    help='after this number of generations the immortals will be randomly chosen again. The default value is 5')

parser.add_argument('-f', '--file', type=str, nargs='?', default='plot.png', const='plot.png',
                    help='name of the output file. Default is plot.png')

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
    series_elite = np.ndarray(shape=(n, gens), dtype=int)
    games = []
    games_elite = []

    for i in range(n):
        state = rng.choice([0, 1], size=shape)
        games.append(GameOfLife(state, norder, ntype))
        games_elite.append(GameOfLife(state, norder, ntype, elite, norder))

    series_tuple = (series, series_elite)
    games_tuple = (games, games_elite)

    for gen in range(gens):
        print(f'Computing generation {gen + 1} of {gens}')
        for i in range(n):
            for s, g in zip(series_tuple, games_tuple):
                s[i][gen] = g[i].count_alive()
                g[i].update()

    print('Ploting series')

    fig, ax = plt.subplots()

    ax.set(xlim=(1, gens),
           xticks=range(1, gens + 1),
           )

    t = np.arange(1, gens + 1)
    color_tuple = ('blue', 'red')
    label_tuple = ('No elite', 'Elite')

    for i in range(n):
        for s, c, l in zip(series_tuple, color_tuple, label_tuple):
            ax.plot(t, s[i], color=c, label=l, lw=0.7, alpha=0.3)
            ax.plot(t, np.mean(s, axis=0), color=c, label=l + ' average')

    handles, labels = ax.get_legend_handles_labels()
    new_labels, new_handles = [], []

    for handle, label in zip(handles, labels):
        if label not in new_labels:
            new_labels.append(label)
            new_handles.append(handle)

    plt.legend(new_handles, new_labels, loc='upper right')

    print(f'Saving image on {filename}')

    plt.savefig(filename, dpi=300)


if __name__ == '__main__':
    main()
