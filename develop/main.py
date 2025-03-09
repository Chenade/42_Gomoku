import pygame, sys
import time
from game import Board, Gomoku
from game.ai import AIPlayer, Node
from setting.config import Config

def handle_move(board, gomoku, move, play_order, player1_score, player2_score):
    board.draw_stone("black" if (play_order) else "white", move)
    player1_score, player2_score, play_order, result = gomoku.move(move, player1_score, player2_score)
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

def init(gomoku, board):
    status = None  # None, "PvP", "PvC"
    play_order = None
    player1_score, player2_score = 0, 0
    ai = None
    board.clean_board()
    gomoku.clean()
    return status, play_order, player1_score, player2_score, ai

if __name__ == "__main__":
        
    pygame.init()
    pygame.font.init()
    setting = Config()
    setting.setup("42 Gomoku")
    gomoku = Gomoku(setting)
    board = Board(setting)

    status, play_order, player1_score, player2_score, ai = init(gomoku, board)

    while True:
        board.draw_button(status)
        board.draw_title(status)
        
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # IS NOT playing
            if status is None:
                # Start the game
                if board.click_button() == "start_pvp":
                    status = "PvP"
                    player1_score, player2_score, play_order = start_new_game(gomoku, board, "PvP")
                if board.click_button() == "start_pvc":
                    status = "PvC"
                    ai = AIPlayer(depth=3)
                    player1_score, player2_score, play_order = start_new_game(gomoku, board, "PvC")

            else:
                # Restart the game
                if board.click_button() == "quit":
                    status, play_order, player1_score, player2_score, ai = init(gomoku, board)

                # Playing
                if play_order is not None:
                    if status == "PvP" or (status == "PvC" and play_order is True):
                        move = board.get_stone_pos(gomoku._stones)
                        if (move is not None):
                            if gomoku.check_legal(move, play_order):
                                player1_score, player2_score, play_order = handle_move(board, gomoku, move, play_order, player1_score, player2_score)
                            else:
                                board.draw_stone("red", move)
                                pygame.display.update()
                                pygame.time.delay(500)
                                board.remove_stone(move)

                        if status == "PvC" and play_order is False:
                            pygame.display.update()
                            move, process_time = gomoku.computer_move(ai, board.draw_stone, board.remove_stone)
                            player1_score, player2_score, play_order = handle_move(board, gomoku, move, play_order, player1_score, player2_score)
                            board.draw_timer(process_time, play_order)  


        pygame.display.update()
