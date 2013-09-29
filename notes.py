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