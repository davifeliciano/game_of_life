import pygame
import numpy as np
from numpy.random import default_rng

from gameoflife import GameOfLife

COLORS = ((189, 147, 249), (80, 250, 123))

class GridRect(pygame.Rect):
    ''' Rect with respective position on the Grid '''
    def __init__(self, rect_pos, rect_dims, pos_in_grid):
        super().__init__(rect_pos, rect_dims)
        self.pos_in_grid = tuple(pos_in_grid)


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
        self.shape = (self._height, self._width)

        if random:
            rng = default_rng()
            state = rng.choice([0, 1], size=self.shape)
        else:
            ''' Create a glider on the top left of the Grid '''
            state = np.zeros(shape=self.shape, dtype=int)

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

    def get_rect(self, pos):
        ''' Returns the rect (if any) of a given position on the screen '''
        indexes = [int(p / (self.offset + self.scale)) for p in pos]
        rect_pos = tuple([index * (self.offset + self.scale) + self.offset for index in indexes])
        rect = GridRect(rect_pos, (self.scale, self.scale), pos_in_grid=indexes)
        return rect

    def handle_mouse(self, pos, mouse_state):
        ''' Takes the position and state of the mouse and draws or erases the respective cell on the screen '''
        rect = self.get_rect(pos)
        
        if rect.collidepoint(*pos):
            j, i = rect.pos_in_grid

            try:
                if mouse_state[0]:
                    self.game.state[i][j] = 1
                    if self.game._generation == 0:
                        self.game.init_state[i][j] = 1

                elif mouse_state[1]:
                    self.game.state[i][j] = 0
                    if self.game._generation == 0:
                        self.game.init_state[i][j] = 0
            except IndexError:
                pass

        self.draw()
        pygame.display.update(rect)

    def draw(self):
        ''' Draw the grid on the screen '''
        for i in range(self._height):
            for j in range(self._width):
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

    def reset(self):
        ''' Reset the Grid to the initial state '''
        self.game.reset()
        self.draw()
        pygame.display.update()
