import pygame

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
    
    setting = Config()
    board = Board(setting)
    gomoku = Gomoku(board)

    while True:
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:

            x_stone, y_stone = board.get_pos()

            # start the game. play order : # True: black, False: white
            if board.w + board.x > x_stone > board.x and board.y + board.h > y_stone > board.y:
                player1_score, player2_score = 0, 0
                _stones, play_order = gomoku.new_game()
                board.text_draw("GAME START", board.w_h//2, 30, setting.palette("green"), 35)

            if play_order is not None:
                board.draw_player(play_order)
                if 45 <= x_stone <= board.w_h and 45 <= y_stone <= board.w_h:
                    x_stone, y_stone = board.get_stone_pos()
            
                    # Draw a white stone
                    if not play_order:
                        _stones = board.draw_stone(_stones, "white", setting.palette("white"), x_stone, y_stone)
                        player1_score, play_order = gomoku.move(_stones, "white", player1_score, play_order)

                    # Draw a black stone
                    elif play_order:
                        _stones = board.draw_stone(_stones, "black", setting.palette("black"), x_stone, y_stone)
                        player2_score, play_order = gomoku.move(_stones, "black", player2_score, play_order)
                    
        board.draw_button()
        pygame.display.update()