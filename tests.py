import unittest

from tictactoe import Game, Board

from datetime import datetime
    


class TestGame(unittest.TestCase):
    
    def setUp(self):
        self.game = Game()        
        
    def test_board_size(self):
        self.assertEqual(len(self.game.board.cells), 9)
    
    def test_check_game_state_premature(self):
        self.assertEqual(self.game.check_game_state(), None)

    def test_check_game_state_no_line(self):
        self.game.move = 6
        self.game.player = 1
        board = self.game.board
        board.cells[0,0].player = 1
        self.assertEqual(self.game.check_game_state(), None)
 
    def test_check_for_winning_row(self):
        self.game.move = 6
        self.game.player = 1
        board = self.game.board
        board.cells[0,0].player = 1
        board.cells[2,0].player = 1
        board.cells[1,0].player = 1
        self.assertEqual(self.game.check_game_state(), 1)

    def test_check_for_winning_column(self):
        self.game.move = 6
        self.game.player = 0
        board = self.game.board
        board.cells[1,0].player = 0
        board.cells[1,1].player = 0
        board.cells[1,2].player = 0
        self.assertEqual(self.game.check_game_state(), 0)

    def test_check_for_winning_diagonal_inc(self):
        self.game.move = 6
        self.game.player = 1
        board = self.game.board
        board.cells[0,0].player = 1
        board.cells[1,1].player = 1
        board.cells[2,2].player = 1
        self.assertEqual(self.game.check_game_state(), 1)

    def test_check_for_winning_diagonal_dec(self):
        self.game.move = 6
        self.game.player = 0
        board = self.game.board
        board.cells[0,2].player = 0
        board.cells[1,1].player = 0
        board.cells[2,0].player = 0
        self.assertEqual(self.game.check_game_state(), 0)

    def test_check_for_draw(self):
        self.game.move = 9
        self.game.player = 0
        self.assertEqual(self.game.check_game_state(), "Draw")

    def test_comprehensive(self):
        combinations = []
        fingerprints = []
    
        combinations.extend([[(x,y) for x in range(3)] for y in range(3)])
        combinations.extend([[(x,y) for y in range(3)] for x in range(3)])
        combinations.extend([[(xy,xy) for xy in range(3)]])
        combinations.extend([[(xy,2-xy) for xy in range(3)]])

        for c in combinations:
            fingerprint = sum([pow(2,x+y*3) for x,y in c])
            fingerprints.append(fingerprint)
        
        board = self.game.board
        for z in range(pow(2,9)-1):
            print "========="
            print z
            for fingerprint in fingerprints:
                print z, fingerprint
                print z & fingerprint
                if z & fingerprint == fingerprint:
                    print "****"



class TestBoard(unittest.TestCase):
    
    def setUp(self):
        self.board = Board() 
               
    def test_get_positions(self):
        board = self.board

        # no cells marked
        self.assertEqual(board.get_positions(0), [])
        
        # a few cells marked
        board.cells[2,0].player = 1
        board.cells[0,0].player = 1
        board.cells[0,1].player = 1
        self.assertEqual(
            set(board.get_positions(1)), 
            set(((0,0), (0,1), (2,0),))
            )
        

class TestCell(unittest.TestCase):
    
    def setUp(self):
        self.game = Game()        
        
    def test_check_for_occupied_cell(self):
        self.assertEqual(self.game.check_game_state(), None)


if __name__ == '__main__':
    unittest.main()
