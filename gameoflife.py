import numpy as np


class GameOfLife():
    '''
    Conway's Game of life

    Attributes

    state : np.ndarray
        integer numpy array with zeros for the dead, ones otherwise.

    shape : tuple
        width and height of state

    elite : float
        number between 0 and 1 that roughtly indicates the percentage of
        the population that will be immortal.

    nstatus : np.ndarray
        integer numpy array showing the status of each individual: one 
        represents a immortal and zero, a mortal. 

    norder : int
        a positive integer representing the size of the neighborhood
        to be considered.

    ntype : str
        the type of neighborhood that will be used to evaluate if
        someone will die or not past a generation. Valid ones are
        'vonneumann' and 'moore'. If none of these are suplied,
        'vonneumann' is assumed.

    neighsize : int
        size of the neighborhood

    '''

    def __init__(self, state, norder=1, ntype='moore', elite=0):

        if isinstance(state, np.ndarray):
            if state.ndim != 2:
                raise ValueError('ndim of state must be 2')
            else:
                self.state = state
        else:
            raise TypeError('state must be a numpy 2-dimensional ndarray')

        self.shape = self.state.shape
        self.width, self.height = self.shape

        if elite < 0 and elite > 1:
            raise ValueError('elite must be a float between 0 and 1')
        else:
            self.elite = elite

        nstatus = np.zeros(shape=self.shape, dtype=int)
        if self.elite:
            for i in range(height):
                for j in range(width):
                    rand = rng.random()
                    if rand < elite:
                        nstatus[i][j] = 1
        self.nstatus = nstatus

        self.norder = abs(norder)

        if ntype == 'vonneumann':
            self.ntype = ntype
            self.neighsize = self.norder ** 2 + (self.norder + 1) ** 2 - 1
        else:
            self.ntype = 'moore'
            self.neighsize = (2 * self.norder + 1) ** 2 - 1

    def __str__(self):
        return f"GameOfLife(shape={self.shape}, ntype='{self.ntype}', elite={self.elite})"

    def show(self):
        print(self.state)

    def count_alive(self):
        return self.state.sum()

    def count_elite(self):
        return self.nstatus.sum()

    def alive_neighbors(self, i0, j0):
        count = 0
        r = self.norder
        range_j = range(- r, r + 1)

        for j in range_j:

            if self.ntype == 'vonneumann':
                r_j = r - abs(j)
                range_i = range(- r_j, r_j + 1)
            if self.ntype == 'moore':
                range_i = range_j

            for i in range_i:
                if j0 + j in range(self.width) and i0 + i in range(self.height):
                    count += self.state[i0 + i][j0 + j]

        if self.state[i0][j0]:
            count -= 1

        return count

    def next_generation(self):
        next_state = np.zeros(shape=self.shape, dtype=int)

        if self.ntype == 'vonneumann' and self.norder == 1:
            upper_tol = 3
            lower_tol = 2
        else:
            upper_tol = self.neighsize / 2
            lower_tol = self.neighsize / 4

        for j in range(self.width):
            for i in range(self.height):
                count = self.alive_neighbors(i, j)
                if self.state[i][j]:
                    if (count >= lower_tol and count < upper_tol):
                        next_state[i][j] = 1
                else:
                    if count > lower_tol and count < upper_tol:
                        next_state[i][j] = 1

        return next_state

    def update(self):
        self.state = self.next_generation()
