import pygame  
import random

COL = 19

class Gomoku:

    def __init__(self, config):
        self.type = None
        self.g_type = None
        self._stones = {}
        COL = config.COL

    def init_board(self):
        self._stones = {}
        for i in range(COL):
            for j in range(COL):
                self._stones[i, j] = 0
        self.play_order = True

    def new_game(self, board, g_type):
        self.g_type = g_type
        board.draw_board()
        self.g_type = g_type
        self.play_order = True
        self.init_board()
        return self.play_order
    
    def clean(self):
        self.g_type = None
        self.init_board()

    def check_win(self, _stones):
        self.result = False
        rows, cols = COL, COL

        def has_continuous_sequence(line):
            count = 0
            last_value = None
            for value in line:
                if value == last_value and value != 0:
                    count += 1
                else:
                    count = 1
                    last_value = value
                if count >= 5:
                    return True
            return False

        # todo: add check breakable by capture

        # Horizontal check
        for i in range(rows):
            row = [ _stones[i, j] for j in range(cols)]
            if has_continuous_sequence(row):
                self.result = True
                return self.result

        # Vertical check
        for j in range(cols):
            column = [ _stones[i, j] for i in range(rows)]
            if has_continuous_sequence(column):
                self.result = True
                return self.result

        # Diagonal check (left to right)
        for i in range(rows - 5):
            for j in range(cols - 5):
                diagonal = [ _stones[i+k, j+k] for k in range(6)]
                if has_continuous_sequence(diagonal):
                    self.result = True
                    return self.result

        # Diagonal check (right to left)
        for i in range(rows - 5):
            for j in range(5, cols):
                diagonal = [ _stones[i+k, j-k] for k in range(6)]
                if has_continuous_sequence(diagonal):
                    self.result = True
                    return self.result

        return self.result


    def check_draw(self, _stones):
        self.result = False
        for i in range(COL):
            for j in range(COL):
                if _stones[i, j] == 0:
                    return self.result
        self.result = True
        return self.result

    def check_legal(self, x_stone, y_stone, play_order):
        if x_stone is not None and y_stone is not None:
            if self._stones[y_stone, x_stone] == 0:
                # todo: add check double three
                self._stones[y_stone, x_stone] = (1 if play_order else 2)
                return True
        return False

    def check_capture(self, _stones):
        # todo: check captures stone's count
        return 1

    def move(self, x_stone, y_stone, play_order, player1_score, player2_score):
        self.play_order = play_order
        self.player1_score, self.player2_score = player1_score, player2_score
        result = None

        captures = self.check_capture(self._stones)
        if captures > 0:
            if not play_order:
                self.player1_score += captures
            else:
                self.player2_score += captures

        check_draw = self.check_draw(self._stones)
        if check_draw:
            result = "DRAW"
            return self.player1_score, self.player2_score, self.play_order, result

        check_win = self.check_win(self._stones)
        if check_win:
            result = "WIN"
            return self.player1_score, self.player2_score, self.play_order, result
           
        self.print_stones()
        self.play_order = not self.play_order
        return self.player1_score, self.player2_score, self.play_order, result

    def print_stones(self):
        for i in range(COL):
            for j in range(COL):
                print(self._stones[i, j], end=" ")
            print()
        print()

    def computer_move(self):
        # pygame.time.delay(1000)
        while True:
            self.x = random.randint(0, COL - 1)
            self.y = random.randint(0, COL - 1)
            if self.check_legal(self.x, self.y, False):
                return self.x, self.y