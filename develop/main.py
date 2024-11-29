import pygame, sys
from game import Board, Gomoku
from setting.config import Config

COL = 19
SIZE = 80

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    _stones = {}
    stones = {}
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
            # start the game
            if gomoku.g_type is None:  # playing
                if board.click_button() == "start_pvp":
                    player1_score, player2_score = 0, 0
                    _stones, play_order = gomoku.new_game(board, "PvP")
                    turn_start_time = pygame.time.get_ticks()  # Initialize timer
                    board.draw_player(gomoku.g_type, play_order)

                if board.click_button() == "start_pvc":
                    player1_score, player2_score = 0, 0
                    _stones, play_order = gomoku.new_game(board, "PvC")
                    turn_start_time = pygame.time.get_ticks()  # Initialize timer
                    board.draw_player(gomoku.g_type, play_order)

            else:
                # restart the game
                if board.click_button() == "quit":
                    play_order = None
                    board.clean_board()
                    gomoku.clean()

                if play_order is not None:
                    if gomoku.g_type == "PvP" or (gomoku.g_type == "PvC" and play_order is True):
                        x_stone, y_stone = board.get_stone_pos()
                        if gomoku.check_legal(x_stone, y_stone):
                            _stones[y_stone, x_stone] = (1 if play_order else 2)
                            board.draw_stone(play_order, x_stone, y_stone)
                            player1_score, player2_score, play_order = gomoku.move(board,_stones, play_order, player1_score, player2_score)
                            turn_start_time = pygame.time.get_ticks()  # Reset timer
                            board.draw_player(gomoku.g_type, play_order)
                            pygame.display.update()
                            if gomoku.g_type == "PvC" and play_order is False:
                                x_stone, y_stone = gomoku.computer_move(_stones)
                                board.draw_stone(play_order, x_stone, y_stone)
                                player1_score, player2_score, play_order = gomoku.move(board,_stones, play_order, player1_score, player2_score)
                                turn_start_time = pygame.time.get_ticks()  # Reset timer
                                board.draw_player(gomoku.g_type, play_order)

        # Timer
        if play_order is not None:
            board.draw_timer(turn_start_time, play_order)
            
        pygame.display.update()
