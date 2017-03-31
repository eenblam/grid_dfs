This is a whiteboard problem a friend posed after receiving it in an interview.

## TODO

- [ ] Add flag for random selection of next neighbor, as opposed to next
- [ ] Refactor `GameInstance` to a general class.
Inherit to produce a grid/matrix game, or a graph game.
- [ ] Separate tests into separate module. Add more.

## Specification
INPUT:
- An mxn matrix with some number of 1 entries. All other entries NULL.
- A starting position.

The 1 entries form a geographic partition of the matrix,
when viewed as a grid on the plane.
The task is to paint the "region" the starting position occurs in with 0s,
without painting cells in other regions.

The starting position should not be labeled with a 1.
Hence, the matrix [[1,1],[1,1]] is illegal.

However, instead of considering such a matrix "illegal,"
we simply declare that any matrix whose entire boundary is labeled with 1s
has been completely painted.

## My Algorithm

```
Initialize an empty stack, $S$.
[A] Label the current position 0.
Examine unlabeled neighbors. Suppose there are $k < 4$ such neighbors.
If $k$ is not 1, i.e. a choice must be made,
then push the current position's coordinates onto the stack $S$.
Pick one arbitrarily. Use random selection or heuristic (e.g. U,R,D,L) as you like.
If $k$ is 1, move to the first element popped from the stack.
If the stack is empty, we are done.
GOTO [A]
```

## Analysis
Suppose $M$ and $N$ are random variables.
Suppose also that the number of 1-valued cells is a random variable $P$.
Suppose that the distribution of $P$ ones is random - 
that is, every cell has the same probability of being 1-valued
as every other cell.

Assume that neighbors are randomly selected, not heuristically selected.
(Hmm... if heuristically selected, do we not get some kind of
local equivalence up to symmetry about a particular point?
The edges of the matrix probably make this untrue,
especially when $m \neg n$.)

Note that fixing $M$, $N$, $P$, and the distribution of $P=p$ ones
still leaves room for multiple traversals.
Does the number of pops differ across traversals?

Consider the following:

- What is the expected size of the stack at a given moment?
- What is the expected number of push (equivalently, pop) operations made?
