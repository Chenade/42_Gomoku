import time
import json


class Game:
    def __init__(self, board_size=19):
        # Initialize a 19x19 board for Gomoku
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.captures = {1: 0, 2: 0}  # Track captures for each player
        self.move_history = []  # Log moves for analysis or undo functionality

    def place_stone(self, x, y, player):
        """Place a stone on the board if the position is empty."""
        if self.board[x][y] == 0:
            self.board[x][y] = player
            self.move_history.append((x, y, player))
            return True
        return False

    def print_board(self):
        """Display the board state in the console."""
        for row in self.board:
            print(" ".join(str(cell) for cell in row))

    def start_timer(self):
        """Start timer for AI move calculation."""
        self.start_time = time.time()

    def end_timer(self):
        """End timer and return the elapsed time."""
        return time.time() - self.start_time

    def check_win(self, player):
        """Check if the given player has won the game."""
        # Check for horizontal, vertical, and diagonal wins
        if (
            self.check_horizontal(player)
            or self.check_vertical(player)
            or self.check_diagonal(player)
        ):
            return True
        if self.captures[player] >= 10:
            return True

        return False

    def check_horizontal(self, player):
        """Check for a horizontal win for the given player."""
        for row in self.board:
            count = 0
            for cell in row:
                if cell == player:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
        return False

    def check_vertical(self, player):
        """Check for a vertical win for the given player."""
        for col in range(self.board_size):
            count = 0
            for row in range(self.board_size):
                if self.board[row][col] == player:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
        return False

    def check_diagonal(self, player):
        """Check for a diagonal win for the given player."""
        # Check for diagonals with positive slope
        for row in range(self.board_size - 4):
            for col in range(self.board_size - 4):
                if all(self.board[row + i][col + i] == player for i in range(5)):
                    return True

        # Check for diagonals with negative slope
        for row in range(4, self.board_size):
            for col in range(self.board_size - 4):
                if all(self.board[row - i][col + i] == player for i in range(5)):
                    return True

        return False
