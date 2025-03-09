from game import Gomoku
from game.ai import AIPlayer

class EventHandler:
    def __init__(self, game):
        self.game = game

    def handle_button(self):
        event = self.game.view.click_button(self.game.status)
        if event is None:
            return self.game.status, self.game.play_order, self.game.player1_score, self.game.player2_score, self.game.ai, self.game.gomoku, False

        if event == "start_pvp":
            self.game.status = "PvP"
            self.game.gomoku = Gomoku(self.game.setting)
            self.game.ai = None
            self.game.player1_score, self.game.player2_score, self.game.play_order = self.game.start_new_game("PvP")
            return self.game.status, self.game.play_order, self.game.player1_score, self.game.player2_score, self.game.ai, self.game.gomoku, True
        if event.startswith("start_pvc"):
            if event == "start_pvc_easy":
                self.game.ai = AIPlayer(depth=1)  # todo: take setting as input
            elif event == "start_pvc_medium":
                self.game.ai = AIPlayer(depth=3)  # todo: take setting as input
            elif event == "start_pvc_hard":
                self.game.ai = AIPlayer(depth=10)  # todo: take setting as input
            self.game.status = "PvC"
            self.game.gomoku = Gomoku(self.game.setting)
            self.game.player1_score, self.game.player2_score, self.game.play_order = self.game.start_new_game("PvC")
            return self.game.status, self.game.play_order, self.game.player1_score, self.game.player2_score, self.game.ai, self.game.gomoku, True
        if event == "quit":
            self.game.ai = None
            self.game.status, self.game.play_order, self.game.player1_score, self.game.player2_score, self.game.ai, self.game.gomoku = self.game.init_game()
            return self.game.status, self.game.play_order, self.game.player1_score, self.game.player2_score, self.game.ai, self.game.gomoku, True
