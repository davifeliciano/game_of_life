import numpy as np
from numpy.random import default_rng
rng = default_rng()


class GameOfLife():
    '''
    Conway's Game of life

    Attributes

    shape : tuple
        width and height of the game.

    state : np.ndarray
        integer numpy array with zeros for the dead, ones otherwise.

    elite : float
        number between 0 and 1 that roughtly indicates the percentage of
        the population that will be immortal.

    status : np.ndarray
        integer numpy array with zeros for the mortals, ones for the elite.

    order : int
        a positive integer representing the size of the neighborhood
        to be considered.

    type : str
        the type of neighborhood that will be used to evaluate if
        someone will die or not past a generation. Valid ones are
        'vonneumann' and 'moore'. If none of these are suplied,
        'vonneumann' is assumed.

    neighbors : int
        size of the neighborhood

    '''

    def __init__(self, width, height, elite=0, order=1, type='vonneumann'):
        self.width = width
        self.height = height
        self.shape = (width, height)
        self.state = rng.choice([0, 1], size=self.shape)

        self.elite = elite

        status = np.zeros(shape=self.shape, dtype=int)
        if self.elite:
            for i in range(height):
                for j in range(width):
                    rand = rng.random()
                    if rand < elite:
                        status[i][j] = 1
        self.status = status

        self.order = order

        if type == 'moore':
            self.type = type
            self.neighbors = (2 * order + 1) ** 2 - 1
        else:
            self.type = 'vonneumann'
            self.neighbors = order ** 2 + (order + 1) ** 2 - 1

    def __str__(self):
        return f"GameOfLife(shape={self.shape}, elite={self.elite}, type='{self.type}')"

    def count_alive(self):
        return self.state.sum()

    def count_elite(self):
        return self.status.sum()

    def alive_neighbors(self, i0, j0):
        count = 0
        r = self.order
        range_j = range(- r, r + 1)

        for j in range_j:

            if self.type == 'vonneumann':
                r_j = r - abs(j)
                range_i = range(- r_j, r_j + 1)
            if self.type == 'moore':
                range_i = range_j

            for i in range_i:
                if j0 + j in range(self.width) and i0 + i in range(self.height):
                    count += self.state[i0 + i][j0 + j]

        if self.state[i0][j0]:
            count -= 1

        return count

    def next_generation(self):
        next_state = np.zeros(shape=self.shape, dtype=int)
        upper_tol = 3 * self.neighbors / 4
        lower_tol = self.neighbors / 2

        for j in range(self.width):
            for i in range(self.height):
                count = self.count_alive()
                if self.state[i][j]:
                    if count < lower_tol or count >= upper_tol:
                        next_state[i][j] = 0
                else:
                    if count > upper_tol:
                        next_state[i][j] = 1

        return next_state

    def update(self):
        self.state = self.next_generation()
