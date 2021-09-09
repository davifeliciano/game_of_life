import numpy as np
from numpy.random import default_rng

rng = default_rng()


class GameOfLife:
    """
    Conway's Game of life

    Attributes

    generation : int
        the generation in which the system is.

    state : np.ndarray
        integer numpy array with zeros for the dead, ones otherwise.
        This array represents the current state of the game.

    init_state : np.ndarray
        integer numpy array with zeros for the dead, ones otherwise.
        This array represents the initial state of the game.

    shape : tuple
        width and height of state.

    elite : float
        number between 0 and 1 that roughtly indicates the percentage of
        the population that will be immortal.

    status : np.ndarray
        integer numpy array showing the status of each individual: one
        represents a immortal and zero, a mortal.

    expec : int
        life expectancy of elite individuals. After this number of
        generations a new status array will be generated.

    norder : int
        a positive integer representing the size of the neighborhood
        to be considered.

    ntype : str
        the type of neighborhood that will be used to evaluate if
        someone will die or not past a generation. Valid ones are
        'vonneumann' and 'moore'. If none of these are suplied,
        'vonneumann' is assumed.

    nsize : int
        size of the neighborhood.
    """

    def __init__(self, state, norder=1, ntype="moore", elite=0.0, expec=1):
        """
        Constructor of GameOfLife

        Parameters

        state : np.ndarray
            integer numpy array with zeros for the dead, ones otherwise.

        norder : int
            a positive non-zero integer representing the size of the neighborhood
            to be considered.

        ntype : str
            the type of neighborhood that will be used to evaluate if
            someone will die or not past a generation. Valid ones are
            'vonneumann' and 'moore'. If none of these are suplied,
            'vonneumann' is assumed.

        elite : float
            number between 0 and 1 that roughtly indicates the percentage of
            the alive population that will be immortal.

        expec : int
            life expectancy of elite individuals. After this number of
            generations a new status array will be generated.
        """

        self._generation = 0

        if state.ndim != 2:
            raise ValueError("ndim of state must be 2")
        else:
            self.init_state = state
            self.state = state

        self.shape = self.state.shape
        self._height, self._width = self.shape

        if norder:
            self.norder = int(abs(norder))
        else:
            self.norder = 1

        if ntype == "vonneumann":
            self._ntype = ntype
            self._nsize = self.norder ** 2 + (self.norder + 1) ** 2 - 1
        else:
            self._ntype = "moore"
            self._nsize = (2 * self.norder + 1) ** 2 - 1

        if elite < 0 and elite > 1:
            raise ValueError("elite must be a float between 0 and 1")
        else:
            self.elite = elite

        if expec:
            self.expec = int(abs(expec))
        else:
            self.expec = 1

        self.status = np.zeros(shape=self.shape, dtype=int)
        self.update_status()
        self.init_status = self.status

    def __repr__(self):
        return f"GameOfLife(shape={self.shape}, ntype='{self.ntype}', elite={self.elite}, expec={self.expec})"

    def update_status(self):
        if self.elite:
            status = np.zeros(shape=self.shape, dtype=int)
            for i in range(self._height):
                for j in range(self._width):
                    if self.state[i][j]:
                        rand = rng.random()
                        if rand < self.elite:
                            status[i][j] = 1
            self.status = status

    @property
    def ntype(self):
        return self._ntype

    @property
    def nsize(self):
        return self._nsize

    def show(self):
        print(self.state)

    def show_init_state(self):
        print(self.init_state)

    def show_status(self):
        print(self.status)

    def count_alive(self):
        return self.state.sum()

    def count_elite(self):
        return self.status.sum()

    def alive_neighbors(self, i0, j0):
        count = 0
        r = self.norder
        range_j = range(-r, r + 1)

        for j in range_j:

            if self.ntype == "vonneumann":
                r_j = r - abs(j)
                range_i = range(-r_j, r_j + 1)
            if self.ntype == "moore":
                range_i = range_j

            for i in range_i:
                if j0 + j in range(self._width) and i0 + i in range(self._height):
                    count += self.state[i0 + i][j0 + j]

        if self.state[i0][j0]:
            count -= 1

        return count

    def next_state(self):
        next_state = np.zeros(shape=self.shape, dtype=int)

        if self.ntype == "vonneumann" and self.norder == 1:
            upper_tol = 3
            lower_tol = 2
        else:
            upper_tol = self.nsize / 2
            lower_tol = self.nsize / 4

        for j in range(self._width):
            for i in range(self._height):
                count = self.alive_neighbors(i, j)
                if self.state[i][j]:
                    if (count >= lower_tol and count < upper_tol) or self.status[i][j]:
                        next_state[i][j] = 1
                else:
                    if (count > lower_tol and count < upper_tol) or self.status[i][j]:
                        next_state[i][j] = 1

        return next_state

    def update(self):
        self._generation += 1
        if self.expec and self._generation % self.expec == 0:
            self.update_status()
        self.state = self.next_state()

    def reset(self):
        self._generation = 0
        self.state = self.init_state
        self.status = self.init_status

    def moving(self):
        """Return True if the next state is different from the current state"""
        if np.array_equal(self.state, self.next_state()):
            return False
        else:
            return True
