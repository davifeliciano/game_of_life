import os
import numpy as np
from time import sleep
from gameoflife import GameOfLife


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def move_cursor(y, x):
    '''Move cursor to position (x, y)'''
    print("\033[%d;%dH" % (y, x))


def game_loop(game, time):
    clear_screen()
    move_cursor(0, 0)
    print(game, '\n')
    game.show()
    while game.moving():
        move_cursor(3, 0)
        game.update()
        game.show()
        sleep(time)

    print('\nDone!')
    sleep(2.0)


glider_state = np.zeros(shape=(15, 15), dtype=int)

glider_state[0][1] = 1
glider_state[1][2] = 1
for j in range(3):
    glider_state[2][j] = 1

glider = GameOfLife(glider_state)

square_state = np.zeros(shape=(15, 15), dtype=int)

for i in range(5, 10):
    for j in range(5, 10):
        square_state[i][j] = 1

square = GameOfLife(square_state)

game_loop(glider, 0.2)
game_loop(square, 0.5)
