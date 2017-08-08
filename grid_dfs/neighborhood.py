class Neighborhood(object):
    def __init__(self):
        self.top = None
        self.right = None
        self.bottom = None
        self.left = None

    def free(self):
        """ Returns a list of all free neighbors.
        """
        return [p for p in self.items() if p.val is None]

    def items(self):
        """ Returns a list of all existing neighbors.

        A None value in the list denotes an off-matrix position.
        """
        l = [self.top, self.right, self.bottom, self.left]
        return [x for x in l if x is not None]

    def next_free(self):
        """ Returns Position of next free neighbor wrt clockwise heuristic
        """
        free = self.free()
        return free[0] if free else None

    def __len__(self):
        """ Returns number of unmarked neighbors
        
        Note that defining __len__ allows truthiness checks
        in which a length of 0 implies the neighborhood is falsey
        """
        return len(self.free())

