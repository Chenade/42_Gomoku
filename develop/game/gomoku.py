import pygame, time
import random
from game.rules.rule_win import check_win
from game.rules.rule_capture import check_capture
from game.rules.rule_double_three import check_double_three

class Gomoku:

    def __init__(self, config):
        self.type = None
        self.g_type = None
        self._stones = []
        self.setting = config
        self.capture = self.setting.CAPTURE
        self.COL = self.setting.COL

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
        board.draw_board(self.setting)
        self.g_type = g_type
        self.play_order = True
        self.init_board()
        return self.play_order
    
    def check_draw(self, _stones):
        self.result = False
        for i in range(self.COL):
            for j in range(self.COL):
                if _stones[i][j] == 0:
                    return self.result
        self.result = True
        return self.result

    def check_legal(self, move, play_order):
        y_stone, x_stone = move
        if x_stone is not None and y_stone is not None:
            if self._stones[y_stone][x_stone] == 0:
                if check_double_three(self.setting, self._stones, move, (-1 if self.play_order else 1)):
                    return False
                self._stones[y_stone][x_stone] = (-1 if play_order else 1)
                return True
        return False

    def move(self, move, player1_score, player2_score):
        capture = check_capture(self.setting, self._stones, move, (-1 if self.play_order else 1))
        if capture:
            for x, y in capture:
                self._stones[x][y] = 3
                if self.play_order:
                    player1_score += 1
                else:
                    player2_score += 1

        if player1_score >= self.capture  or player2_score >= self.capture or \
            check_win(self._stones, self.COL, self.COL):
            return player1_score, player2_score, self.play_order, "WIN"
        
        # self.print_stones()
        self.play_order = not self.play_order
        return player1_score, player2_score, self.play_order, None

    def computer_move(self, ai, draw_stone, remove_stone):
        start_time = time.time()
        top_moves = ai.get_top_moves(self._stones, current_player=1, top_n=3)
        end_time = time.time()
        process_time = end_time - start_time
        
        draw_stone("white", top_moves[0][1])

        # suggest #2 moves
        draw_stone("_white", top_moves[1][1])

        # suggest #3 moves
        draw_stone("_white", top_moves[2][1])

        pygame.display.update()

        # remove #2, #3 moves after 1 second
        pygame.time.delay(1000)
        remove_stone(top_moves[1][1])
        remove_stone(top_moves[2][1])  

        self.check_legal(top_moves[0][1], self.play_order)
        return top_moves[0][1], process_time
    
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