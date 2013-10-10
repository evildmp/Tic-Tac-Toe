import unittest

from datetime import datetime

from tictactoe import Game, Board, WinningLine


class TestGame(unittest.TestCase):
    def test_check_game_when_not_enough_moves(self):
        game = Game(dimensions=(6,6))
        self.assertEqual(game.check_game_state(), None)

    def test_check_game_we_have_run_out_of_moves(self):
        game = Game(dimensions=(6,6))
        game.move = 36
        with self.assertRaises(SystemExit) as cm:
            game.check_game_state()
        self.assertEqual(cm.exception.code, "It's a draw")

class TestBoard(unittest.TestCase):

    def test_we_can_set_a_board_size_directly(self):
        board = Board(dimensions=(3,3))
        self.assertEqual(len(board.cells), 9)

    def test_set_board_size_through_game(self):
        game = Game(dimensions=(10,10))
        self.assertEqual(len(game.board.cells), 100)

    def test_create_cells(self):
        board = Board(dimensions=(3,3))
        for y in range(0,3):
            for x in range(0,3):
                self.assertTrue((x,y) in board.cells)
                self.assertEqual(
                    board.cells[(x,y)].board,
                    board
                    )

    def test_get_positions_of_0_none(self):
        board = Board(dimensions=(3,3), winning_length=3)
        self.assertEqual(
            board.get_positions(player=0),
            [])

    def test_get_positions_all_empty(self):
        board = Board(dimensions=(3,3), winning_length=3)
        self.assertItemsEqual(
            board.get_positions(player=None),
            board.cells
            )

    def test_get_positions_multiple(self):
        board = Board(dimensions=(3,3), winning_length=3)
        for x in range(0,3):
            board.cells[(x,1)].mark(player=0)
        for y in range(0,3):
            board.cells[(1,y)].mark(player=1)

        self.assertItemsEqual(
            board.get_positions(player=0),
            [(0, 1), (2, 1)]
            )
        self.assertItemsEqual(
            board.get_positions(player=1),
            [(1, 0), (1, 1), (1,2)]
            )
        self.assertItemsEqual(
            board.get_positions(player=None),
            [(0,0), (2,0), (0,2), (2,2)]
            )

    def test_create_lines(self):
        board = Board(dimensions=(0,0))
        line = board.create_line(start=(0,7), vector=(1,-1), length=8)
        self.assertEqual(
            line,
            [(0, 7), (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)]
        )

    def test_calculate_winning_lines_3(self):
        board = Board(dimensions=(3,3), winning_length=3)
        self.assertEqual(
            board.calculate_winning_lines(),
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

    def test_calculate_winning_lines_2(self):
        board = Board(dimensions=(3,3), winning_length=2)
        self.assertEqual(
            board.calculate_winning_lines(),
            [
                # vertical pairs (top)
                [(0, 0), (0, 1)],
                [(1, 0), (1, 1)],
                [(2, 0), (2, 1)],
                # vertical pairs (bottom)
                [(0, 1), (0, 2)],
                [(1, 1), (1, 2)],
                [(2, 1), (2, 2)],
                # diagonal pairs (top)
                [(0, 0), (1, 1)],
                [(1, 0), (2, 1)],
                # diagonal pairs (bottom)
                [(0, 1), (1, 2)],
                [(1, 1), (2, 2)],
                # horizontal pairs (top)
                [(0, 0), (1, 0)],
                [(1, 0), (2, 0)],
                # horizontal pairs (middle)
                [(0, 1), (1, 1)],
                [(1, 1), (2, 1)],
                # horizontal pairs (bottom)
                [(0, 2), (1, 2)],
                [(1, 2), (2, 2)],
                # diagonal pairs (middle)
                [(0, 1), (1, 0)],
                [(1, 1), (2, 0)],
                # diagonal pairs (bottom)
                [(0, 2), (1, 1)],
                [(1, 2), (2, 1)],
            ]
        )

    def test_create_winning_lines(self):
        board = Board(dimensions=(10,10), winning_length=2)
        self.assertEqual(
            [wl.cells for wl in board.winning_lines],
            board.calculate_winning_lines()
            )

    def test_get_fingerprint(self):
        board = Board(dimensions=(3,3), winning_length=3)
        for x in range(0,3):
            board.cells[(x,1)].mark(player=0)
        for y in range(0,3):
            board.cells[(1,y)].mark(player=1)
        # player 0 has bits 3,5 set = 40
        self.assertEqual(board.get_fingerprint(player=0), 40)
        # player 1 has bits 1,4,7 set = 146
        self.assertEqual(board.get_fingerprint(player=1), 146)

    def test_check_for_winning_line(self):
        board = Board(dimensions=(3,3), winning_length=3)
        for x in range(0,3):
            board.cells[(x,1)].mark(player=0)
        self.assertTrue(board.check_for_winning_line(player=0))

        for y in range(0,3):
            board.cells[(1,y)].mark(player=1)
        self.assertTrue(board.check_for_winning_line(player=1))
        self.assertFalse(board.check_for_winning_line(player=0))

    def test_identify_winning_moves(self):
        board = Board(dimensions=(3,3), winning_length=3)
        board.cells[(0,1)].mark(player=0)
        board.cells[(1,1)].mark(player=0)

        board.cells[(0,0)].mark(player=1)
        board.cells[(2,0)].mark(player=1)

        board.cells[(2,2)].mark(player=1)
        board.cells[(1,2)].mark(player=1)

        possibles = board.get_positions(player=None)
        self.assertItemsEqual(
            board.identify_winning_moves(player=0, possibles=possibles),
            [(2,1)]
        )

        possbles = board.get_positions(player=None)
        self.assertItemsEqual(
            board.identify_winning_moves(player=1, possibles=possibles),
            [(2,1), (1,0), (0,2)]
        )

        board = Board(dimensions=(3,3), winning_length=3)
        board.cells[(0,0)].mark(player=1)
        board.cells[(2,2)].mark(player=1)

        possibles = board.get_positions(player=None)
        self.assertItemsEqual(
            board.identify_winning_moves(player=1, possibles=possibles),
            [(1,1)]
        )

    def test_identify_win_creators(self):
        board = Board(dimensions=(3,3), winning_length=3)
        board.cells[(0,0)].mark(player=0)
        board.cells[(2,2)].mark(player=0)
        board.cells[(1,1)].mark(player=1)
        possibles = board.get_positions(player=None)
        self.assertItemsEqual(
            board.identify_win_creators(player=0, possibles=possibles),
            [(0,2), (2,0)]
        )

    def test_choose_next_move_to_win(self):
        # winning move available at (1,1)
        board = Board(dimensions=(3,3), winning_length=3)
        board.cells[(0,0)].mark(player=0)
        board.cells[(2,2)].mark(player=0)
        board.choose_next_move(player=0)
        self.assertEqual(
            board.winners,
            [(1, 1)]
        )

    def test_choose_next_move_to_win_we_lose(self):
        # winning move available at (1,1)
        board = Board(dimensions=(3,3), winning_length=3)
        board.cells[(0,0)].mark(player=0)
        board.cells[(2,2)].mark(player=0)
        board.choose_next_move(player=1)
        self.assertEqual(
            board.losers,
            [(1, 1)]
        )


    def test_choose_next_move_to_win_spot_multiple_winners(self):
        # 3 winning moves available at (1,1), (1,0), (2,1)
        board = Board(dimensions=(3,3), winning_length=3)
        board.cells[(0,0)].mark(player=0)
        board.cells[(2,0)].mark(player=0)
        board.cells[(2,2)].mark(player=0)
        board.choose_next_move(player=0)
        self.assertEqual(
            set(board.winners),
            set(((2, 1), (1, 0), (1, 1)))
        )
    #
    # def test_choose_next_move_to_prevent_opponent_win(self):
    #     # opponent has winning move available at (1,1)
    #     board = Board(dimensions=(3,3), winning_length=3)
    #     board.cells[(0,0)].mark(player=0)
    #     board.cells[(2,2)].mark(player=0)
    #     possibles = board.get_positions(player=None)
    #     self.assertEqual(
    #         board.choose_next_move(player=1, possibles=possibles),
    #         ("avoid losing", (1,1))
    #     )
    #
    # def test_choose_next_move_to_block_one_winning_move(self):
    #     # opponent has winning move available at (1,1) and
    #     board = Board(dimensions=(3,3), winning_length=3)
    #     board.cells[(0,0)].mark(player=0)
    #     board.cells[(2,0)].mark(player=0)
    #     board.cells[(0,2)].mark(player=0)
    #     possibles = board.get_positions(player=None)
    #     next_move = board.choose_next_move(player=1, possibles=possibles)
    #     self.assertEqual(next_move[0], "hope to avoid losing")
    #     self.assertTrue(next_move[1] in [(0,1), (1,0), (1,1)])
    #
    # def test_choose_next_move_win_creator(self):
    #     # can win on the next move with (0,2) or (2,0)
    #     board = Board(dimensions=(3,3), winning_length=3)
    #     board.cells[(0,0)].mark(player=0)
    #     board.cells[(2,2)].mark(player=0)
    #     board.cells[(1,1)].mark(player=1)
    #     possibles = board.get_positions(player=None)
    #     next_move = board.choose_next_move(player=0, possibles=possibles)
    #     self.assertEqual(next_move[0], "win next")
    #     self.assertTrue(
    #         next_move[1] in [(0,2), (2,0)])
    #
    # def test_choose_next_win_open(self):
    #     board = Board(dimensions=(4,4), winning_length=3)
    #     board.cells[(0,0)].mark(player=0)
    #     possibles = board.get_positions(player=None)
    #     board.choose_next_move(player=1, possibles=possibles)

class TestWinningLine(unittest.TestCase):
    def test_has_correct_fingerprint(self):
        """
        We can't test every possible fingerprint, but we can provide
        a few sample test cases
        """
        board = Board(dimensions=(1,3), winning_length=3)
        # bits 0,1,2
        w = WinningLine([(0,0,), (0,1), (0,2)], board)
        self.assertEqual(w.fingerprint, 7)

        board = Board(dimensions=(3,1), winning_length=3)
        # bits 0,1,2
        w = WinningLine([(0,0,), (1,0), (2,0)], board)
        self.assertEqual(w.fingerprint, 7)

        board = Board(dimensions=(3,3), winning_length=3)
        # bits 0,5,8
        w = WinningLine([(0,0,), (0,1), (0,2)], board)
        self.assertEqual(w.fingerprint, 73)



if __name__ == '__main__':
    unittest.main()
