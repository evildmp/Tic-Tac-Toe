class Game(object):
    def check_game_state(self):
        # returns None, player 0 or player 1

        # don't even bother checking if we haven't yet had 6 moves
        if self.move > 5:

            # find all the positions this player occupies
            positions = self.board.get_positions(self.player)

            # find starts of all potential winning lines
            # they all start at x=0 or y=0
            for (x,y) in [p for p in positions]:
                # for each starting position, find the line-mates that would
                # make a winning line
                all_line_mates = [
                    [(x+r,y) for r in range(3)],     # row
                    ((x,y+1), (x,y+2)),     # column
                    ((x+1,y+1), (x+2,y+2)), # diagonal
                    ((x+1,y-1), (x+2,y-2))  # other diagonal
                    ]
                # if the player occupies all the cells in any of the line-mates,
                # we have a winner
                for line_mates in all_line_mates:
                    if set(line_mates) <= set(positions):
                        sys.exit("%s wins" %PLAYERS[self.player])

        # we have exhausted all possible moves; it's a draw
        if self.move >= 8:
            sys.exit("It's a draw")

# draw the board
PLAYERS = {0: "x", 1: "o", None: ""}

    def draw(self):
        print
        print "\n-----\n".join(["|".join([PLAYERS[self.cells[(x,y)].player] or str(y*3+x) for x in range(0,3)]) for y in range(0,3)])


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
        self.board.draw()
        if self.board.game.check_game_state() != None:

             "Winner", self.board.game.check_game_state()
            sys.exit()
        self.board.game.player = -cmp(self.board.game.player, 1)
        self.board.game.move += 1
