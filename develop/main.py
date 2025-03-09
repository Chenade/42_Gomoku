import pygame, sys
import time
from game import Board, Gomoku
from game.ai import AIPlayer, Node
from setting.config import Config

COL = 19
SIZE = 80

def handle_move(board, gomoku, x_stone, y_stone, play_order, player1_score, player2_score):
    board.draw_stone("black" if (play_order) else "white", x_stone, y_stone)
    player1_score, player2_score, play_order, result = gomoku.move(x_stone, y_stone, player1_score, player2_score)
    board.remove_captures(gomoku._stones)
    board.draw_player(gomoku.g_type, play_order, player1_score, player2_score)
    if result is not None:
        board.draw_result(gomoku.g_type, gomoku.play_order, result)
        play_order = None
    return player1_score, player2_score, play_order

def start_new_game(gomoku, board, game_type):
    player1_score, player2_score = 0, 0
    play_order = gomoku.new_game(board, game_type)
    board.draw_player(gomoku.g_type, play_order, player1_score, player2_score)
    return player1_score, player2_score, play_order

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    player1_score, player2_score = 0, 0
    play_order = None
    setting = Config()
    setting.setup("42 Gomoku")
    board = Board(setting)
    gomoku = Gomoku(setting)
    ai = AIPlayer(depth=3)

    while True:
        event = pygame.event.poll()
        board.draw_button(gomoku.g_type)
        board.draw_title(gomoku.g_type)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # IS NOT playing
            if gomoku.g_type is None:
                # Start the game
                if board.click_button() == "start_pvp":
                    player1_score, player2_score, play_order = start_new_game(gomoku, board, "PvP")
                if board.click_button() == "start_pvc":
                    player1_score, player2_score, play_order = start_new_game(gomoku, board, "PvC")

            else:
                # Restart the game
                if board.click_button() == "quit":
                    play_order = None
                    board.clean_board()
                    gomoku.clean()

                # Playing
                if play_order is not None:
                    if gomoku.g_type == "PvP" or (gomoku.g_type == "PvC" and play_order is True):
                        x_stone, y_stone = board.get_stone_pos()
                        if gomoku.check_legal(x_stone, y_stone, play_order):
                            player1_score, player2_score, play_order = handle_move(board, gomoku, x_stone, y_stone, play_order, player1_score, player2_score)
                        else:
                            board.draw_stone("red", x_stone, y_stone)
                            pygame.display.update()
                            pygame.time.delay(500)
                            board.remove_stone(x_stone, y_stone)

                        if gomoku.g_type == "PvC" and play_order is False:
                            pygame.display.update()
                            x_stone, y_stone, process_time = gomoku.computer_move(ai, board.draw_stone, board.remove_stone)
                            player1_score, player2_score, play_order = handle_move(board, gomoku, x_stone, y_stone, play_order, player1_score, player2_score)
                            board.draw_timer(process_time, play_order)  


        pygame.display.update()
