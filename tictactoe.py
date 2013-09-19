import sys
from random import choice

class Game(object):
    
    def __init__(self, players=None):
        self.players = players
        self.player = 0
        self.move = 0
        self.board = Board(self)
        self.board.draw()

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
            
    STRATEGIES = {
        "random": "play_random_move",
        "first": "play_first_available_move",
            "winning": "choose_winning_move",
    }        

    def play(self, strategy="random"):
        # so far, we only cater for 0-player games
        if not self.players:
            getattr(self, self.STRATEGIES[strategy])()
            self.play(strategy)     
    
    # different strategies for playing 
    
    def play_first_available_move(self):
        position = self.board.get_positions(None)[0]
        self.board.cells[position].mark()
        
    def play_random_move(self):
        position = choice(self.board.get_positions(None))
        self.board.cells[position].mark()
        
    def choose_winning_move(self):
        self.play_random_move()
        
        
class Board(object):

    def __init__(self, game=None):
        self.game = game
        
        self.cells = {}
        for y in range(0,3):
            for x in range(0,3):
                self.cells[(x,y)] = Cell(self)

    def draw(self):
        print
        print "\n-----\n".join(["|".join([PLAYERS[self.cells[(x,y)].player] or str(y*3+x) for x in range(0,3)]) for y in range(0,3)])
        
    
    def get_positions(self, player):
        # Get a list of the cells the player has moved into;
        # player = None for unoccupied cells
        return [
            position for position, cell in self.cells.items() if cell.player==player
            ]


    # untested
    def get_cell(self, position):
        return self.cells[position]


    def __str__(self):
        for x in range(0,3):
            for y in range(0,3):
                print self.cells[(x,y)],
            print
        return str(self.game.player) 


PLAYERS = {0: "x", 1: "o", None: ""}

class Cell(object):

    def __init__(self, board):
        self.board = board
        self.player = None
        
    def __repr__(self):
        return PLAYERS.get(self.player)

    def mark(self):
        # marks a cell for a player
        self.player = self.board.game.player
        self.board.draw()
        if self.board.game.check_game_state() != None:
            print "Winner", self.board.game.check_game_state()
            sys.exit()
        self.board.game.player = -cmp(self.board.game.player, 1)
        self.board.game.move += 1
               
               
game = Game()
# game.play("winning")
