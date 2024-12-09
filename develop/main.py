import pygame, sys
from game import Board, Gomoku
from setting.config import Config

COL = 19
SIZE = 80

def handle_move(board, gomoku, x_stone, y_stone, play_order, player1_score, player2_score):
    board.draw_stone(play_order, x_stone, y_stone)
    player1_score, player2_score, play_order, result = gomoku.move(x_stone, y_stone, player1_score, player2_score)
    board.draw_player(gomoku.g_type, play_order, player1_score, player2_score)
    if result is not None:
        board.draw_result(gomoku.g_type, gomoku.play_order, result)
        play_order = None
    return player1_score, player2_score, play_order

def start_new_game(gomoku, board, game_type):
    player1_score, player2_score = 0, 0
    play_order = gomoku.new_game(board, game_type)
    turn_start_time = pygame.time.get_ticks()  # Initialize timer
    board.draw_player(gomoku.g_type, play_order, player1_score, player2_score)
    return player1_score, player2_score, play_order, turn_start_time

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    player1_score, player2_score = 0, 0
    play_order = None
    turn_start_time = None  # Timer start time
    setting = Config()
    setting.setup("42 Gomoku")
    board = Board(setting)
    gomoku = Gomoku(setting)

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
                    player1_score, player2_score, play_order, turn_start_time = start_new_game(gomoku, board, "PvP")
                if board.click_button() == "start_pvc":
                    player1_score, player2_score, play_order, turn_start_time = start_new_game(gomoku, board, "PvC")

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
                            turn_start_time = pygame.time.get_ticks()  # Reset timer

                        if gomoku.g_type == "PvC" and play_order is False:
                            pygame.display.update()
                            x_stone, y_stone = gomoku.computer_move()
                            player1_score, player2_score, play_order = handle_move(board, gomoku, x_stone, y_stone, play_order, player1_score, player2_score)
                            turn_start_time = pygame.time.get_ticks()  # Reset timer

        # Timer
        if play_order is not None:
            board.draw_timer(turn_start_time, play_order)

        pygame.display.update()
