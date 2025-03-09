import pygame, sys
import time
from game import Board, Gomoku
from game.ai import AIPlayer, Node
from setting.config import Config

def handle_move(view, gomoku, move, play_order, player1_score, player2_score):
    view.draw_stone("black" if (play_order) else "white", move)
    player1_score, player2_score, play_order, result = gomoku.move(move, player1_score, player2_score)
    view.remove_captures(gomoku._stones)
    view.draw_player(gomoku.g_type, play_order, player1_score, player2_score)
    if result is not None:
        view.draw_result(gomoku.g_type, gomoku.play_order, result)
        play_order = None
    return player1_score, player2_score, play_order

def start_new_game(gomoku, view, game_type):
    player1_score, player2_score = 0, 0
    play_order = gomoku.new_game(view, game_type)
    view.draw_player(gomoku.g_type, play_order, player1_score, player2_score)
    return player1_score, player2_score, play_order

def init(view):
    status = None  # None, "PvP", "PvC"
    play_order = None
    player1_score, player2_score = 0, 0
    ai = None
    gomoku = None
    view.clean()
    return status, play_order, player1_score, player2_score, ai, gomoku

if __name__ == "__main__":
        
    pygame.init()
    pygame.font.init()
    setting = Config("42 Gomoku")
    view = Board(setting)

    status, play_order, player1_score, player2_score, ai, gomoku = init(view)

    while True:
        view.draw_button(status)
        view.draw_title(status)

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # IS NOT playing
            if status is None:
                # Start the game
                if view.click_button() == "start_pvp":
                    status = "PvP"
                    # setting.change_column(10)
                    gomoku = Gomoku(setting)
                    player1_score, player2_score, play_order = start_new_game(gomoku, view, "PvP")
                if view.click_button() == "start_pvc":
                    status = "PvC"
                    # setting.change_column(10)
                    gomoku = Gomoku(setting)
                    ai = AIPlayer(depth=3) ## todo: take setting as config
                    player1_score, player2_score, play_order = start_new_game(gomoku, view, "PvC")

            else:
                # Restart the game
                if view.click_button() == "quit":
                    status, play_order, player1_score, player2_score, ai, gomoku = init(view)

                # Playing
                if play_order is not None:
                    if status == "PvP" or (status == "PvC" and play_order is True):
                        move = view.get_stone_pos(gomoku._stones)
                        if (move is not None):
                            if gomoku.check_legal(move, play_order):
                                player1_score, player2_score, play_order = handle_move(view, gomoku, move, play_order, player1_score, player2_score)
                            else:
                                view.draw_stone("red", move)
                                pygame.display.update()
                                pygame.time.delay(500)
                                view.remove_stone(move)

                        if status == "PvC" and play_order is False:
                            pygame.display.update()
                            move, process_time = gomoku.computer_move(ai, view.draw_stone, view.remove_stone)
                            player1_score, player2_score, play_order = handle_move(view, gomoku, move, play_order, player1_score, player2_score)
                            view.draw_timer(process_time, play_order)  


        pygame.display.update()
