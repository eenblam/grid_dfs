#!/usr/bin/env python
from itertools import chain
from random import randint, sample

from PIL import Image, ImageSequence

from neighborhood import Neighborhood
from position import Position

class GameInstance(object):
    def __init__(self, m, n, M=None):
        #TODO Flag for heuristic/clockwise/deterministic stepping
        # Random preferable for simulation, but deterministic needed for testing
        self.m = m
        self.n = n
        if M is not None:
            self.__original__ = M
        else:
            self.__random_matrix__()
        self.M = self.__original__
        self.__verify_matrix__()
        self.stack = []
        self.position = None

    def __boundary_has_opening__(self):
        """ Returns True if input matrix has opening in boundary
        """
        orig = self.__original__
        top = all(x == 1 for x in orig[0])
        bottom = all(x == 1 for x in orig[-1])
        ends = chain.from_iterable((row[0], row[-1]) for row in orig[1:-1])
        ends = all(x == 1 for x in ends)
        return not (top and bottom and ends)

    def __random_matrix__(self):
        m = self.m
        n = self.n
        M = [[]] * m
        for i in range(m):
            M[i] = [None] * n
            for j in range(n):
                if sample((0,1), 1)[0]:
                    M[i][j] = 1

        self.__original__ = M

    def __verify_matrix__(self):
        orig = self.__original__
        if len(orig) != self.m:
            raise ValueError("Input matrix M does not have m={} rows"
                            .format(self.m))
        if not all(len(row) == self.n for row in orig):
            raise ValueError("Input matrix M does not have n={} columns"
                            .format(self.n))

    def complete(self):
        """ Return True when no moves are available or matrix is an island
        """
        if not self.__boundary_has_opening__():
            return True
        elif self.position is None:
            return False

        # Nontrivial boundary and game initialized
        has_neighbors = bool(self.neighbors())
        has_stack = bool(self.stack)
        return not (has_neighbors or has_stack)

    def mark(self, i=None, j=None, val=0):
        try:
            i = self.position.i if i is None else i
            j = self.position.j if j is None else j
        except AttributeError:
            raise ValueError("Start not set. Either set start or provide coordinates to mark.")

        try:
            self.M[i][j] = val
        except IndexError:
            raise ValueError("Cannot mark ({}, {}) with value {}"
                            .format(i, j, val))

    def neighbors(self, i=None, j=None):
        """ Construct and return Neighborhood of point if point is exists
        """
        if not self.position_exists(i, j):
            raise ValueError("Position ({}, {}) does not exist in a {} x {} matrix"
                            .format(i, j, self.m, self.n))

        if (i is None) != (j is None):
            # Only one coordinate provided
            raise ValueError("Cannot get neighbors of a column or row")

        if i == j == None and self.position is None:
            # Both None
            raise ValueError("Cannot retrieve neighbors. Either set start or provide coordinates to mark.")

        i, j, _ = self.position

        nbhd = Neighborhood()
        # Keep things ordered clockwise for consistency in code
        # Top
        if i > 0:
            nbhd.top = Position(i-1, j, self.M[i-1][j])
        # Right
        if j < self.n-1:
            nbhd.right = Position(i, j+1, self.M[i][j+1])
        # Bottom
        if i < self.m-1:
            nbhd.bottom = Position(i+1, j, self.M[i+1][j])
        # Left
        if j > 0:
            nbhd.left = Position(i, j-1, self.M[i][j-1])

        return nbhd

    def position_exists(self, i=None, j=None):
        """ Return validity of input coordinates.
        """
        i = i if i is not None else 0
        j = j if j is not None else 0
        i_okay = 0 <= i < self.m
        j_okay = 0 <= j < self.n
        return i_okay and j_okay

    def set_start(self, i=None, j=None):
        """ Set a starting position, random if no inputs specified.
        """
        if not self.position_exists(i, j):
            raise ValueError("Cannot start at position ({}, {}) in {} x {} matrix"
                            .format(i, j, self.m, self.n))

        if i is None or j is None:
            return self.random_start(i, j)

        # Deterministic start
        if self.M[i][j]:
            raise ValueError("Cannot start in 1-valued position ({}, {})"
                            .format(i, j))

        self.mark(i, j)
        self.position = Position(i, j, 0)
        return

    def __random_coord__(self):
        return randint(0, self.m), randint(0, self.n)

    def random_start(self, i=None, j=None):
        if not self.position_exists(i, j):
            raise ValueError("Cannot start at position ({}, {}) in {} x {} matrix"
                            .format(i, j, self.m, self.n))

        if not self.__boundary_has_opening__():
            # We're only setting the start
            # There's no error to throw,
            # as a complete game should just complete immediately
            self.position = None
            return

        val = True
        while val is not None:
            i_r = randint(0, self.m - 1) if i is None else i
            j_r = randint(0, self.n - 1) if j is None else j
            val = self.M[i_r][j_r]

        self.mark(i_r, j_r)
        self.position = Position(i_r, j_r, 0)
        return

    def reset(self):
        # Reset M
        self.M = self.__original__

    def show_simulation(self, steps=None, pause=False):
        for state in self.simulate(steps):
            print(state)
            if pause:
                _ = raw_input()

    def step(self):
        nb = self.neighbors()
        population= len(nb)

        if population > 1:
            self.stack.append(self.position)

        if population:
            self.position = nb.next_free()
            self.mark()
        elif self.stack:
            self.position = self.stack.pop()
            self.mark()
        else:
            # No population, no stack => complete => do nothing
            return

    def __str__(self):
        def lines():
            for row in self.M:
                row = ('x' if x is None else str(x) for x in row)
                line = ' '.join(row) + '\n'
                yield line

        i,j,_ = self.position if self.position is not None else None, None, None
        if self.position is None:
            pos_str = 'Position:\tNone\n'
        else:
            pos_str = 'Position:\t({}, {})\n'.format(self.position.i, self.position.j)

        return pos_str + ''.join(lines())

    def gif(self, fname, steps=None):
        sim = self.simulate(steps)
        frames = [state.__gif_frame__() for state in sim]
        first, rest = frames[0], frames[1:]
        if fname[-4:] != '.gif':
            raise ValueError('Filename is not a .gif')

        with open(fname, 'w') as f:
            first.save(f, save_all=True, append_images=rest)


    def __gif_frame__(self):
        im = Image.new("RGB", (self.m, self.n), None)
        x, y, _ = self.position
        pos = x * self.n + y

        flat_M_RGB = list(colorify(x) for x in chain.from_iterable(self.M))
        # Paint current position red
        flat_M_RGB[pos] = (256,0,0)

        im.putdata(flat_M_RGB)
        size = (self.m * 100, self.n * 100)
        im.resize(size)
        im = im.transform(size, Image.EXTENT, (0,0, size[0], size[1]))

        return im



    def simulate(self, steps=None):
        if self.complete():
            return

        if self.position is None:
            self.random_start()

        if steps is None:
            while not self.complete():
                yield self
                self.step()
        else:
            for i in range(steps):
                yield self
                self.step()

        yield self

def colorify(x):
    if x is None:
        # Unvisited, unwalled - Black
        return (0,0,0)
    if x == 1:
        # Walled - White
        return (256,256,256)
    if x == 0:
        # Visited - Grey
        return (128,128,128)
    # Error - Blue
    return (0,0,256)

