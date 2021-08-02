import pygame
import numpy as np
from numpy.random import default_rng

from gameoflife import GameOfLife

COLORS = ((189, 147, 249), (80, 250, 123))


class Grid():
    '''
    Grid to draw a Game of Life in a pygame surface

    Attributes

    surface : pygame Surface
        surface where the Grid will bre drawn.

    scale : int
        the width and height of a cell in the grid, in pixels.

    offset : int
        the distance between each cell in the grid, in pixels.

    colors : 2-tuple
        tuple with two colors. The first is for the alive cells
        and the second is for the elite cells.

    height, width and shape: int, int and 2-tuple
        the dimensions of the grid generated based on the size
        of the provided Surface.

    game : GameOfLife
        the game that will be drawn to the surface.
    '''

    def __init__(self, surface, scale=20, offset=2, colors=COLORS, random=False, elite=False):
        '''
        Constructor of Grid

        Parameters

        surface : pygame Surface
            surface where the Grid will bre drawn.

        scale : int
            the width and height of a cell in the grid, in pixels.

        offset : int
            the distance between each cell in the grid, in pixels.

        colors : 2-tuple
            tuple with two colors. The first is for the alive cells
            and the second is for the elite cells.

        random : Bool
            if True, Grid.game will be initialized with a random matrix.
            if False, it will be initialized with a glider.

        elite : Bool
            if True, Grid.game will be initialized with elite=0.05 and
            expec=5
        '''

        self.surface = surface
        self.scale = scale
        self.offset = offset
        self.colors = colors

        surface_height = self.surface.get_height()
        surface_width = self.surface.get_width()

        self._height = int(surface_height / (self.scale + self.offset))
        self._width = int(surface_width / (self.scale + self.offset))
        self._shape = (self.height, self.width)

        if random:
            rng = default_rng()
            state = rng.choice([0, 1], size=self._shape)
        else:
            state = np.zeros(shape=self._shape, dtype=int)

            state[1][2] = 1
            state[2][3] = 1

            for j in range(1, 4):
                state[3][j] = 1

        if elite:
            elite = 0.05
            expec = 5
        else:
            elite = 0.0
            expec = 1

        self.game = GameOfLife(state, elite=elite, expec=expec)

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def shape(self):
        return self._shape

    def draw(self):

        for i in range(self.height):
            for j in range(self.width):
                x = j * (self.offset + self.scale)
                y = i * (self.offset + self.scale)

                color = self.colors[0]

                if self.game.state[i][j]:
                    width = 0
                else:
                    width = 1

                if self.game.status[i][j]:
                    color = self.colors[1]
                    width = 0

                pygame.draw.rect(self.surface, color,
                                 [x + self.offset,
                                     y + self.offset,
                                     self.scale,
                                     self.scale],
                                 width=width,
                                 border_radius=3)
