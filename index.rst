=================================
Tic-Tac-Toe, or Noughts & Crosses
=================================

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
