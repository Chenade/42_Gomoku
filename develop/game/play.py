import pygame  
import random

COL = 19
SIZE = 80

class Gomoku:

    def __init__(self):
        self.type = None
        self.g_type = None

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
            if self.check_legal(self.x, self.y):
                self.stones[self.y, self.x] = 2
                return self.x, self.y