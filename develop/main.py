import pygame
import sys
from game import Game
from event import EventHandler

def main():
    pygame.init()
    pygame.font.init()
    game = Game()
    event_handler = EventHandler(game)
    # game.setting.set_column(5)
    # game.setting.set_color(board_color="dark_green", line_color="white")

    while True:
        game.view.draw_page(game.status)

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            game.status, game.play_order, game.player1_score, game.player2_score, game.ai, game.gomoku, button_clicked = event_handler.handle_button()
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
                check_draw = game.gomoku.check_draw(game.gomoku._stones)
                if check_draw:
                    game.view.text_result(game.gomoku.g_type, game.gomoku.play_order, "DRAW")
                    game.play_order = None

        pygame.display.update()

if __name__ == "__main__":
    main()