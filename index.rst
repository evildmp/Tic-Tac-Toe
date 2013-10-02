=================================
Tic-Tac-Toe, or Noughts & Crosses
=================================

We - human beings - have the concept of a line, irreducible to relationships
between points.

Can this be represented natively at the level of Python code?

If not, could it be represented through a higher-level object that represents
it internally as a collection of points on a Cartesian grid (and would this be
worth the effort anyway?)

It seems hard to justify the effort required to describe a line in general,
when all that matters are *winning* lines. We use the concept of 'lineness'
while playing, but it's not actually part of the conceptual space of the game
itself.

Look-ahead
==========

Recursing up the tree:

    Given the current state of the board, is there a move I can make that would
    win? Put it in the winning pile.

    Of the other moves:
        is there one that leaves the opponent with a winning move? Put it in the
        reject pile.

        is there one that leaves the opponent with a losing move? Put it in the
        winning pile.

        Hypothesise each of the other moves, and each possible response of the
        opponent. Given the current state of the board...

What are we going to do with this information?

Another way of looking ahead
----------------------------

A guaranteed winning position is one that allows me to complete more than one
line in a single move, as long as my opponent can't win on the next move.

Strategies
==========

Has this player won?
--------------------

Only check the last move!
^^^^^^^^^^^^^^^^^^^^^^^^^

... and not the whole board.

Is this a winning line?
^^^^^^^^^^^^^^^^^^^^^^^

Use board-specific logic
........................

* easy for 3x3 board
* ... not extendable to larger/other boards

Walk all the possibilities from here
....................................

* not nice logic

Match binary fingerprints
.........................

* make each cell a bit, and the board a number
* calculate the binary fingerprint of each winning line
* check for the fingerprint in the board
* we can generate winning combinations in advance, for use in tests (unless we
  know all winning combinations in advance, we can't easily test algorithms
  that test for wins)
