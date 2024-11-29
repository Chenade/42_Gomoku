import pygame  
import random

COL = 19

class Gomoku:

    def __init__(self, config):
        self.type = None
        self.g_type = None
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
        board.draw_score(0, 0)
        self.g_type = g_type
        self.play_order = True
        self.init_board()
        return self._stones, self.play_order
    
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

    def check_legal(self, x_stone, y_stone):
        if x_stone is not None and y_stone is not None:
            if self._stones[y_stone, x_stone] == 0:
                # todo: add check double three
                return True
        return False

    def move(self, board, stones, play_order, player1_score, player2_score):
        self.stones, self.play_order = stones, play_order
        self.player1_score, self.player2_score = player1_score, player2_score
        self.result = None

        check_draw = self.check_draw(self.stones)
        if check_draw:
            board.draw_result(self.g_type, self.play_order, "DRAW")
            self.result = True
            self.play_order = None
            return self.player1_score, self.player2_score, None

        check_win = self.check_win(self.stones)
        if check_win:
            board.draw_result(self.g_type, self.play_order, "WIN")
            self.result = True
            self.play_order = None
            return self.player1_score, self.player2_score, None
           
        self.print_stones()
        self.play_order = not self.play_order
        return self.player1_score, self.player2_score, self.play_order

    def print_stones(self):
        for i in range(COL):
            for j in range(COL):
                print(self.stones[i, j], end=" ")
            print()
        print()

    def computer_move(self, stones):
        self.stones = stones
        # pygame.time.delay(1000)
        while True:
            self.x = random.randint(0, COL - 1)
            self.y = random.randint(0, COL - 1)
            if self.check_legal(self.x, self.y):
                self.stones[self.y, self.x] = 2
                return self.x, self.y