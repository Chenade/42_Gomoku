import pygame
import sys
from setting.config import Config
from game import View, Gomoku
from game.ai import AIPlayer
from event import EventHandler

class Game:
    def __init__(self, setting):
        self.setting = setting
        self.view = View(setting)
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
        self.view.draw_stone("black" if self.play_order else "white", move)
        self.player1_score, self.player2_score, self.play_order, result = self.gomoku.move(move, self.player1_score, self.player2_score)
        self.view.remove_captures(self.gomoku._stones)
        self.view.text_player(self.gomoku.g_type, self.play_order, self.player1_score, self.player2_score)
        if result is not None:
            self.view.text_result(self.gomoku.g_type, self.gomoku.play_order, result)
            self.play_order = None
        return self.player1_score, self.player2_score, self.play_order

def main():
    pygame.init()
    pygame.font.init()
    setting = Config("42 Gomoku")
    game = Game(setting)
    event_handler = EventHandler(game)

    while True:
        game.view.draw_page(game.status)

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            game.status, game.play_order, game.player1_score, game.player2_score, game.ai, game.gomoku, button_clicked = event_handler.handle_button_event()
            if button_clicked:
                continue

            # Playing
            if game.play_order is not None:
                if game.status == "PvP" or (game.status == "PvC" and game.play_order is True):
                    move = game.view.get_stone_pos(game.gomoku._stones)
                    if move is not None:
                        if game.gomoku.check_legal(move, game.play_order):
                            game.player1_score, game.player2_score, game.play_order = game.handle_move(move)
                        else:
                            game.view.draw_stone("red", move)
                            pygame.display.update()
                            pygame.time.delay(500)
                            game.view.remove_stone(move)

                    if game.status == "PvC" and game.play_order is False:
                        pygame.display.update()
                        move, process_time = game.gomoku.computer_move(game.ai, game.view.draw_stone, game.view.remove_stone)
                        game.player1_score, game.player2_score, game.play_order = game.handle_move(move)
                        game.view.text_timer(process_time, game.play_order)

        pygame.display.update()

if __name__ == "__main__":
    main()