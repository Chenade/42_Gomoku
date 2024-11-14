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
                self._stones[(SIZE * i, SIZE * j)] = 0
        return self._stones, True

    def check_win(self, stone_sort):
        self.result = False
        for x, y in stone_sort:
            cnt = 0
            for i in range(1, 5):
                if (x, y + SIZE * i) in stone_sort:
                    cnt += 1
                    if cnt == 4:
                        self.result = True
                        break

                else: break

            cnt = 0
            for i in range(1, 5):
                if (x + SIZE * i, y) in stone_sort:
                    cnt += 1
                    if cnt == 4:
                        self.result = True
                        break
                else: break

            cnt = 0
            for i in range(1, 5):
                if (x + SIZE * i, y+SIZE * i) in stone_sort:
                    cnt += 1
                    if cnt == 4:
                        self.result = True
                        break
            cnt = 0
            for i in range(1, 5):
                if (x + SIZE * i, y - SIZE * i) in stone_sort:
                    cnt += 1
                    if cnt == 4:
                        self.result = True
                        break

        return self.result

    # def check_legal(self, stone, color_name):

    def move(self, stone, color_name, player_score, play_order):
        self.stones, player_color, self.player_score = stone, color_name, player_score
        self.play_order = play_order
        self.result = None

        if len(self.stones["white"]) + len(self.stones["black"]) == 225:
            self.play_order = self.result(None, "DRAW")
            return self.player_score, self.play_order

        if len(self.stones[player_color]) >= 5:

            stone_sort = sorted(self.stones[player_color])
            check_win = self.check_win(stone_sort)
            if check_win:
                self.result = True
                self.play_order = None
                self.player_score += 1
                self.board.draw_result(color_name, "WIN")
                return self.player_score, self.play_order
           
        self.play_order = not self.play_order
        return self.player_score, self.play_order