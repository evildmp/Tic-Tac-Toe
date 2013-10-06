import sys
import copy
import random

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
    def __init__(self, game=None, dimensions=(), winning_length=0, cells=None):
        self.game = game
        self.winning_length=winning_length
        self.cells = cells or {}

        # board dimensions must be declared
        self.dimensions = dimensions or self.game.dimensions
        self.x, self.y = self.dimensions[0], self.dimensions[1]

        if not self.cells:
            self.create_cells()  # sets self.cells
        self.create_winning_lines()  # sets self.winning_lines

    def create_cells(self):
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
        if player != None:
            fingerprint = self.get_fingerprint(player)
            # print "player fingerprint", fingerprint
            for wl in self.winning_lines:
                # print "wl fp", wl.fingerprint, fingerprint & wl.fingerprint
                if fingerprint & wl.fingerprint == wl.fingerprint:
                    # print "match", wl.fingerprint
                    return True

    def identify_winning_moves(self, player, possibles=None):
        """docstring for identify_winning_moves"""
        # get possible moves
        possibles = possibles or []
        winners = []
        # which of the possibles makes a winning line?
        for possible in possibles:
            hypothetical = copy.deepcopy(self)
            hypothetical.cells[possible].player=player
            if hypothetical.check_for_winning_line(player=player):
                winners.append(possible)
        return winners

    def identify_win_creators(self, player, possibles=None):
        possibles = possibles or []
        win_creators = []
        for possible in possibles:
            hypothetical = copy.deepcopy(self)
            hypothetical.cells[possible].player=player
            hypothetical_possibles = hypothetical.get_positions(player=None)
            wms = hypothetical.identify_winning_moves(player=player, possibles=hypothetical_possibles)
            if len(wms) > 1:
                win_creators.append(possible)
        return win_creators

    def choose_next_move(self, player, possibles=None):
        possibles = possibles or []

        # first deal with the case where we can win
        winners = self.identify_winning_moves(player, possibles)
        if winners:
            return "win", random.choice(winners)

        # the case where we block the opponent's winning move
        opponent_winners = self.identify_winning_moves(player=-cmp(player, 1), possibles=possibles)
        if opponent_winners:
            if len(opponent_winners) == 1:
                return "avoid losing", opponent_winners[0]

            # this is just temporary; it won't do as a real solution
            # even if this is a 'losing' position, we should aim for the best
            # response anyway; the opponent might make a mistake
            # if the opponent has more than one way to win, just hope for the best
            else:
                return "hope to avoid losing", random.choice(opponent_winners)

        # a case where neither can win on this go, but we can set a win for
        # the next move
        win_creators = self.identify_win_creators(player=player, possibles=possibles)
        if win_creators:
            return "win next", random.choice(win_creators)

        else:
            # so far untested

            # for all the things we might do, see what the opponent's best
            # response is
            for possible in possibles:
                hypothetical = copy.deepcopy(self)
                hypothetical.cells[possible].player=player
                opponents_best = hypothetical.choose_next_move(player=-cmp(player, 1))
                if "hope" in opponents_best[0]:
                    return "win", possible

                # we should never get here
                if "win" in opponents_best[0]:
                    raise Exception



class Cell(object):

    def __init__(self, board=None, player=None):
        self.board = board
        self.player = player

    def mark(self, player=None):
        # marks a cell for a player
        if player == None:
            self.player = self.board.game.player
        else:
            self.player = player


# game = Game()
# game.play("winning")
