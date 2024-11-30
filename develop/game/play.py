import pygame  
import random
from game.rule_win import check_win
from game.rule_capture import check_capture

class Gomoku:

    def __init__(self, config):
        self.type = None
        self.g_type = None
        self._stones = {}
        self.COL = config.COL

    def init_board(self):
        self._stones = {}
        for i in range(self.COL):
            for j in range(self.COL):
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

    def check_draw(self, _stones):
        self.result = False
        for i in range(self.COL):
            for j in range(self.COL):
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

    # return player1_score, player2_score_play_order, result(text)
    def move(self, x_stone, y_stone, player1_score, player2_score):
        if self.play_order:
            player1_score += check_capture(self._stones, self.COL, self.COL)
        else:
            player2_score += check_capture(self._stones, self.COL, self.COL)

        if player1_score > 4  or player2_score > 4 or \
            check_win(self._stones, self.COL, self.COL):
            return player1_score, player2_score, self.play_order, "WIN"
        
        if self.check_draw(self._stones):
            return player1_score, player2_score, self.play_order, "DRAW"

        self.print_stones()
        self.play_order = not self.play_order
        return player1_score, player2_score, self.play_order, None

    def print_stones(self):
        for i in range(self.COL):
            for j in range(self.COL):
                print(self._stones[i, j], end=" ")
            print()
        print()

    def computer_move(self):
        # pygame.time.delay(1000)
        while True:
            self.x = random.randint(0, self.COL - 1)
            self.y = random.randint(0, self.COL - 1)
            if self.check_legal(self.x, self.y, False):
                return self.x, self.y