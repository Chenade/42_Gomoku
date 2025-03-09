import pygame, time
import random
# from config import Config
from game.rules.rule_win import check_win
from game.rules.rule_capture import check_capture
from game.rules.rule_double_three import check_double_three
from setting.config import Config

class Gomoku:

    def __init__(self, config):
        self.type = None
        self.g_type = None
        self._stones = []
        self.COL = config.COL
        # self.capture = Config.CAPTURE
        # print(self.capture)

    def init_board(self):
        self._stones = {}
        self._stones = [0] * self.COL
        for i in range(self.COL):
            self._stones[i] = [0] * self.COL
            # for j in range(self.COL):
                # self._stones[i][j] = 0
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
                if _stones[i][j] == 0:
                    return self.result
        self.result = True
        return self.result

    def check_legal(self, x_stone, y_stone, play_order):
        move = (y_stone, x_stone)
        if x_stone is not None and y_stone is not None:
            if self._stones[y_stone][x_stone] == 0:
                if check_double_three(self._stones, move, (-1 if self.play_order else 1)):
                    return False
                self._stones[y_stone][x_stone] = (-1 if play_order else 1)
                return True
        return False

    def move(self, x_stone, y_stone, player1_score, player2_score):
        
        move = (y_stone, x_stone)
        capture = check_capture(self._stones, move, (-1 if self.play_order else 1))
        if capture:
            for x, y in capture:
                self._stones[x][y] = 3
                if self.play_order:
                    player1_score += 1
                else:
                    player2_score += 1

        if player1_score >= 10  or player2_score >= 10 or \
            check_win(self._stones, self.COL, self.COL):
            return player1_score, player2_score, self.play_order, "WIN"
        
        self.print_stones()
        self.play_order = not self.play_order
        return player1_score, player2_score, self.play_order, None

    def print_stones(self):
        print("   | ", end="")
        for i in range(self.COL):
            print(" ", end="")
            print(i, end=" ")
        print("\n---------------------------------------------------------------------")
        for i in range(self.COL):
            if (i < 10):
                print(" ", end="")
            print(f"{i} | ", end="")
            for j in range(self.COL):
                if (j >= 10):
                    print(" ", end="")
                if self._stones[i][j] != -1:
                    print(" ", end="")
                print(self._stones[i][j], end=" ")
            print()
        print()

    def computer_move(self, ai, draw_stone, remove_stone):
        start_time = time.time()
        top_moves = ai.get_top_moves(self._stones, current_player=1, top_n=3)
        end_time = time.time()
        process_time = end_time - start_time
        
        print(top_moves)
        r_y_stone, r_x_stone = top_moves[0][1]
        
        # suggest #1 moves(x_stone, y_stone)
        print(r_x_stone, r_y_stone)
        draw_stone("white", r_x_stone, r_y_stone)

        # suggest #2 moves
        y_stone, x_stone = top_moves[1][1]
        print(x_stone, y_stone)
        draw_stone("_white", x_stone, y_stone)

        # suggest #3 moves
        y_stone, x_stone = top_moves[2][1]
        print(x_stone, y_stone)
        draw_stone("_white", x_stone, y_stone)

        pygame.display.update()

        # remove #2, #3 moves after 1 second
        pygame.time.delay(1000)
        remove_stone(x_stone, y_stone)
        y_stone, x_stone = top_moves[1][1]
        remove_stone(x_stone, y_stone)  
        
        return r_x_stone, r_y_stone, process_time