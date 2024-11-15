import pygame  


COL = 19
SIZE = 80

class Gomoku:

    def __init__(self, board):
        self.board = board
        self.setting = self.board.setting

    def new_game(self):
        self.board.draw_board()
        self.board.draw_score(0, 0)
        
        self._stones = {}
        for i in range(COL):
            for j in range(COL):
                self._stones[i, j] = 0
        return self._stones, True

    def check_win(self, _stones):
        self.result = False
        return self.result

    # def check_legal(self, stone, color_name):

    def move(self, stones, color_name, player_score, play_order):
        self.stones, player_color, self.player_score = stones, color_name, player_score
        self.play_order = play_order
        self.result = None

        check_win = self.check_win(self.stones)
        if check_win:
            self.result = True
            self.play_order = None
            self.player_score += 1
            self.board.draw_result(color_name, "WIN")
            return self.player_score, self.play_order
           
        self.print_stones()
        self.play_order = not self.play_order
        return self.player_score, self.play_order

    def print_stones(self):
        for i in range(COL):
            for j in range(COL):
                print(self.stones[i, j], end=" ")
            print()
        print()