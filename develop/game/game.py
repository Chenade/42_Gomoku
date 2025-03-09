
from game import View
from setting.config import Config

class Game:
    def __init__(self):
        self.setting = Config("42 Gomoku")
        self.view = View(self.setting)
        self.status, self.play_order, self.player1_score, self.player2_score, self.ai, self.gomoku = self.init_game()

    def init_game(self):
        status = None  # None, "PvP", "PvC"
        play_order = None
        player1_score, player2_score = 0, 0
        ai = None
        gomoku = None
        self.view.clean_page()
        return status, play_order, player1_score, player2_score, ai, gomoku

    def start_new_game(self, game_type):
        self.player1_score, self.player2_score = 0, 0
        self.play_order = self.gomoku.new_game(self.view, game_type)
        self.view.text_player(self.gomoku.g_type, self.play_order, self.player1_score, self.player2_score)
        return self.player1_score, self.player2_score, self.play_order

    def handle_move(self, move):
        self.view.draw_stone("player1" if self.play_order else "player2", move)
        self.player1_score, self.player2_score, self.play_order, result = self.gomoku.move(move, self.player1_score, self.player2_score)
        self.view.remove_captures(self.gomoku._stones)
        self.view.text_player(self.gomoku.g_type, self.play_order, self.player1_score, self.player2_score)
        if result is not None:
            self.view.text_result(self.gomoku.g_type, self.gomoku.play_order, result)
            self.play_order = None
        return self.player1_score, self.player2_score, self.play_order
