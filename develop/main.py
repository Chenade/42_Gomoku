import pygame

from game import Gomoku
from setting.config import Config 

COL = 19
SIZE = 80

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    stone = {}
    stone["white"], stone["black"] = [], []
    player1_score, player2_score = 0, 0
    setting = Config()
    game = Gomoku(setting)  
    game.draw_board()
    game.draw_player(None)
    game.draw_score(player1_score, player2_score)

    play_order = None
    start = False

    while True:
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:

            x_stone, y_stone = game.play_get_pos()

            # start the game.
            if game.w + game.x > x_stone > game.x and game.y + game.h > y_stone > game.y:
                stone["white"], stone["black"] = [], []
                player1_score, player2_score = 0, 0
                game = Gomoku(setting)
                game.draw_board()
                game.draw_score(player1_score, player2_score)
                game.text_draw("GAME START", game.w_h//2, 30, setting.palette("green"), 35)
                play_order = True
                game.draw_player(play_order)

            if play_order is not None:
                game.draw_player(play_order)
            
                # Draw a white stone (Player 1).
                if not play_order:
                    if 45 <= x_stone <= game.w_h and 45 <= y_stone <= game.w_h:
                        x_stone, y_stone = game.play_draw_stone_pos()
                        stone, play_order = game.play_draw_stone( stone, play_order, "white", setting.palette("white"), x_stone, y_stone)
                        player1_score, play_order = game.score(stone, "white", player1_score, play_order)
                        if len(stone["white"]) + len(stone["black"]) == 225:
                            game.text_draw("DRAW", 80 * 22 + 65, game.w_h // 2 + 120, (200, 0, 0), 45)
                            play_order = None

                # Draw a black stone (Player 2).
                elif play_order:
                    if 45 <= x_stone <= game.w_h and 45 <= y_stone <= game.w_h:
                        x_stone, y_stone = game.play_draw_stone_pos()
                        stone, play_order = game.play_draw_stone(stone, play_order, "black", setting.palette("black"), x_stone, y_stone)

                        player2_score, play_order = game.score( stone, "black", player2_score, play_order)
                        if len(stone["white"]) + len(stone["black"]) == 225:
                            game.text_draw("DRAW", 80 * 22 + 65, game.w_h//2 + 120,(200, 0, 0), 45)
                            play_order = None

            
        game.draw_button()
        pygame.display.update()