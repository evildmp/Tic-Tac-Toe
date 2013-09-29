import unittest

from datetime import datetime

from tictactoe import Game, Board


class TestBoard(unittest.TestCase):

    def test_we_can_set_a_board_size_directly(self):
        board = Board(dimensions=(3,3))
        self.assertEqual(len(board.cells), 9)

    def test_set_board_size_through_game(self):
        game = Game(dimensions=(10,10))
        self.assertEqual(len(game.board.cells), 100)

    def test_create_lines(self):
        board = Board(dimensions=(0,0))
        line = board.create_line(start=(0,7), vector=(1,-1), length=8)
        self.assertEqual(
            line,
            [(0, 7), (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)]
        )

    def test_create_winning_lines_3x3(self):
        board = Board(dimensions=(3,3), winning_length=3)
        self.assertEqual(
            board.winning_lines,
            [
                # 3 columns
                [(0,0,), (0,1), (0,2)],
                [(1,0,), (1,1), (1,2)],
                [(2,0,), (2,1), (2,2)],
                # diagonal
                [(0,0,), (1,1), (2,2)],
                # 3 rows
                [(0,0,), (1,0), (2,0)],
                [(0,1,), (1,1), (2,1)],
                [(0,2,), (1,2), (2,2)],
                # other diagonal
                [(0,2,), (1,1), (2,0)],
            ]
            )

    def test_create_winning_lines_2x2(self):
        board = Board(dimensions=(2,2), winning_length=2)
        self.assertEqual(
            board.winning_lines,
            [
                # 2 columns
                [(0,0,), (0,1)],
                [(1,0,), (1,1)],
                # diagonal
                [(0,0,), (1,1)],
                # 2 rows
                [(0,0,), (1,0)],
                [(0,1,), (1,1)],
                # other diagonal
                [(0,1,), (1,0)],
            ]
            )

    # def test_winning_lines_are_correct(self):
    #     # For a given board, check that it knows what its
    #     # winning lines are. We can't check them all, but we can
    #     # check a few
    #     board = Board(dimensions=(3,3))
    #     self.assertTrue((0,1), (0,2), (0,3) in board.winninglines)

#     def test_check_game_state_premature(self):
#         self.assertEqual(self.game.check_game_state(), None)
#
#     def test_check_game_state_no_line(self):
#         self.game.move = 6
#         self.game.player = 1
#         board = self.game.board
#         board.cells[0,0].player = 1
#         self.assertEqual(self.game.check_game_state(), None)
#
#     def test_check_for_winning_row(self):
#         self.game.move = 6
#         self.game.player = 1
#         board = self.game.board
#         board.cells[0,0].player = 1
#         board.cells[2,0].player = 1
#         board.cells[1,0].player = 1
#         with self.assertRaises(SystemExit) as cm:
#             self.game.check_game_state()
#         self.assertEqual(cm.exception.code, "o wins")
#
#     def test_check_for_winning_column(self):
#         self.game.move = 6
#         self.game.player = 0
#         board = self.game.board
#         board.cells[1,0].player = 0
#         board.cells[1,1].player = 0
#         board.cells[1,2].player = 0
#         with self.assertRaises(SystemExit) as cm:
#             self.game.check_game_state()
#         self.assertEqual(cm.exception.code, "x wins")
#
#     def test_check_for_winning_diagonal_inc(self):
#         self.game.move = 6
#         self.game.player = 1
#         board = self.game.board
#         board.cells[0,0].player = 1
#         board.cells[1,1].player = 1
#         board.cells[2,2].player = 1
#         with self.assertRaises(SystemExit) as cm:
#             self.game.check_game_state()
#         self.assertEqual(cm.exception.code, "o wins")
#
#     def test_check_for_winning_diagonal_dec(self):
#         self.game.move = 6
#         self.game.player = 0
#         board = self.game.board
#         board.cells[0,2].player = 0
#         board.cells[1,1].player = 0
#         board.cells[2,0].player = 0
#         with self.assertRaises(SystemExit) as cm:
#             self.game.check_game_state()
#         self.assertEqual(cm.exception.code, "x wins")
#
#     def test_check_for_draw(self):
#         self.game.move = 9
#         self.game.player = 0
#         with self.assertRaises(SystemExit) as cm:
#             self.game.check_game_state()
#         self.assertEqual(cm.exception.code, "It's a draw")
#
#
# class TestBoard(unittest.TestCase):
#
#     def setUp(self):
#         self.board = Board()
#
#     def test_get_positions(self):
#         board = self.board
#
#         # no cells marked
#         self.assertEqual(board.get_positions(0), [])
#
#         # a few cells marked
#         board.cells[2,0].player = 1
#         board.cells[0,0].player = 1
#         board.cells[0,1].player = 1
#         self.assertEqual(
#             set(board.get_positions(1)),
#             set(((0,0), (0,1), (2,0),))
#             )
#
#
#     def test_board_has_correct_winning_line_fingerprints(self):
#         combinations = []
#         fingerprints = []
#
#         combinations.extend([[(x,y) for x in range(3)] for y in range(3)])
#         combinations.extend([[(x,y) for y in range(3)] for x in range(3)])
#         combinations.extend([[(xy,xy) for xy in range(3)]])
#         combinations.extend([[(xy,2-xy) for xy in range(3)]])
#
#         for c in combinations:
#             fingerprint = sum([pow(2,x+y*3) for x,y in c])
#             fingerprints.append(fingerprint)
#
#         self.assertEqual(
#             [w.fingerprint for w in self.board.winninglines],
#             fingerprints
#             )
#
#
# class TestCell(unittest.TestCase):
#
#     def setUp(self):
#         self.game = Game()
#
#     def test_check_for_occupied_cell(self):
#         self.assertEqual(self.game.check_game_state(), None)
#
#

if __name__ == '__main__':
    unittest.main()
