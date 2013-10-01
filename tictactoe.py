import sys
from random import choice

class Game(object):
    """
    A Game is the total game environment - the board, its cells, its states,
    the players, their moves and the rules through which they stand in relation
    to each other
    """
    def __init__(self, dimensions=None, winning_length=0, players=None):
        self.board = Board(self, dimensions, winning_length)

        self.player = 0
        self.move = 0

        self.players = players
        # self.board.draw()

    def check_game_state(self):
        # returns None, player 0 or player 1

        # don't even bother checking if we haven't yet had enough moves
        if self.move < self.board.winning_length * 2 - 1:
            return

        # we have exhausted all possible moves; it's a draw
        if self.move >= self.board.x * self.board.y -1:
            sys.exit("It's a draw")


class WinningLine(object):
    def __init__(self, cells, board):
        self.cells = cells
        self.fingerprint = sum(
            [pow(2,x+y*board.dimensions[0])
            for x,y in cells]
            )


class Board(object):
    def __init__(self, game=None, dimensions=(), winning_length=0):
        self.game = game
        self.winning_length=winning_length

        # board dimensions must be declared
        self.dimensions = dimensions or self.game.dimensions
        self.x, self.y = self.dimensions[0], self.dimensions[1]

        self.create_cells()
        self.create_winning_lines()

    def create_cells(self):
        self.cells = {}
        for y in range(0,self.y):
            for x in range(0,self.x):
                self.cells[(x,y)] = Cell(self)

    def create_winning_lines(self):
        self.winning_lines = [
            WinningLine(line, self)
            for line in self.calculate_winning_lines()
            ]

    def calculate_winning_lines(self):
        # the vectors are four of eight points of the compass
        # we don't need their reflections
        winning_lines=[]
        vectors = ((0,1), (1,1), (1,0), (1,-1))
        for v in vectors:
            for y in range(self.y):
                for x in range(self.x):
                    # Check if line will be within board dimensions
                    # These checks are coupled to the vectors above - using the
                    # vectors' reflections would require additional checks.
                    if x + v[0] * self.winning_length <= self.x and \
                        y + v[1] * self.winning_length <= self.y and \
                        1 + y + v[1] * self.winning_length >= 0:
                        start = (x,y)
                        winning_lines.append(
                            self.create_line(start, v, self.winning_length)
                            )
        return winning_lines

    def create_line(self, start, vector, length):
        return [
        (
            start[0] + vector[0] * l,
            start[1] + vector[1] * l
            )
        for l in range(length)
        ]

    def get_positions(self, player):
        # Get a list of the cells the player has moved into;
        # player = None for unoccupied cells
        return [
            pos for pos, cell in self.cells.items() if cell.player==player
            ]

    def get_fingerprint(self, player):
        return sum(
            [pow(2,x+y*self.dimensions[0])
            for x,y in self.get_positions(player)
            ])

    def check_for_winning_line(self, player=None, cell=None):
        if not player == None:
            fingerprint = self.get_fingerprint(player)
            for wl in self.winning_lines:
                if fingerprint & wl.fingerprint:
                    return True


class Cell(object):

    def __init__(self, board):
        self.board = board
        self.player = None

    def mark(self, player=None):
        # marks a cell for a player
        if player == None:
            self.player = self.board.game.player
        else:
            self.player = player


# game = Game()
# game.play("winning")
