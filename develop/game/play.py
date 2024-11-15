import pygame  
import random

COL = 19
SIZE = 80

class Gomoku:

    def __init__(self):
        self.type = None
        # self.board = board
        # self.setting = self.board.setting

    def new_game(self, board, g_type):
        self.g_type = g_type
        board.draw_board()
        board.draw_score(0, 0)
        self.g_type = g_type
        
        self._stones = {}
        for i in range(COL):
            for j in range(COL):
                self._stones[i, j] = 0
        self.play_order = True
        return self._stones, self.play_order

    def check_win(self, _stones):
        self.result = False
        return self.result

    def check_draw(self, _stones):
        self.result = False
        for i in range(COL):
            for j in range(COL):
                if _stones[i, j] == 0:
                    return self.result
        self.result = True
        return self.result

    # def check_legal(self, stone, color_name):

    def move(self, board, stones, play_order, player1_score, player2_score):
        self.stones, self.play_order = stones, play_order
        self.player1_score, self.player2_score = player1_score, player2_score
        self.result = None

        check_draw = self.check_draw(self.stones)
        if check_draw:
            self.result = True
            self.play_order = None
            board.draw_result(self.g_type, self.play_order, "DRAW")
            return self.player1_score, self.player2_score, None

        check_win = self.check_win(self.stones)
        if check_win:
            self.result = True
            self.play_order = None
            self.player_score += 1
            board.draw_result(self.g_type, self.play_order, "WIN")
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
            if self.stones[self.y, self.x] == 0:
                self.stones[self.y, self.x] = 2
                return self.x, self.y