import pygame

class Text:
    def __init__(self, screen, setting):
        self.screen = screen
        self.button_size = setting.button_size
        self.font_size = setting.font_size
        self.get_color = setting.get_color
        self.panel_x = setting.panel_x
        self.w_h = setting.w_h

    def text_draw(self, text, pos, font_color):
        x_pos, y_pos = pos
        self.text = text
        self.font_color = self.get_color(font_color)
        ff = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        TextSurf, TextRect = self.text_objects(self.text, ff, self.font_color)
        TextRect.center = (x_pos, y_pos)
        self.screen.blit(TextSurf, TextRect)

    def text_objects(self, text, font, font_color):
        textSurface = font.render(text, True, font_color)
        return textSurface, textSurface.get_rect()

    def draw_title(self, status):
        panel_x = self.panel_x
        if status is not None:
            pos = (panel_x + 120, self.font_size)
            self.text_draw("GOMOKU", pos, "black")
            pos = (panel_x + 120, self.font_size * 2)
            if status == "PvP":
                self.text_draw("Player against Player", pos, "green")
            elif status == "PvC":
                self.text_draw("Player against Computer", pos, "green")
        else:
            # draw text
            font = pygame.font.Font(None, self.font_size * 2)
            text = font.render("GOMOKU", True, self.get_color("black"))
            width, height = self.screen.get_size()

            text_rect = text.get_rect(center=(width // 2, height // 2 - self.font_size * 3 - 100))
            self.screen.blit(text, text_rect)

    def draw_player(self, g_type, play_order, player1_score, player2_score):
        panel_x = self.panel_x
        w_h = self.w_h

        pos_player_1 = (panel_x + 120, w_h // 2 - 100)
        pos_player_2 = (panel_x + 120, w_h // 2 + 100)
        if g_type == "PvP":
            if play_order:
                self.text_draw("PLAYER 1", pos_player_1, "red")
                self.text_draw("PLAYER 2", pos_player_2, "black")
            elif not play_order:
                self.text_draw("PLAYER 1", pos_player_1, "black")
                self.text_draw("PLAYER 2", pos_player_2, "red")
        else:
            if play_order:
                self.text_draw("PLAYER", pos_player_1, "red")
                self.text_draw("COMPUTER", pos_player_2, "black")
            elif not play_order:
                self.text_draw("PLAYER", pos_player_1, "black")
                self.text_draw("COMPUTER", pos_player_2, "red")

        pygame.draw.circle(self.screen, self.get_color("black"), (panel_x, w_h // 2 - 50), self.font_size)
        pygame.draw.circle(self.screen, self.get_color("white"), (panel_x, w_h // 2 + 150), self.font_size)

        # Draw score
        pygame.draw.rect(self.screen, self.get_color("board"), (panel_x + 70, w_h // 2 - 80, 80, 80))
        pos = (panel_x + 120, w_h // 2 - 40)
        self.text_draw(str(player1_score), pos, "black")

        pygame.draw.rect(self.screen, self.get_color("board"), (panel_x + 90, w_h // 2 + 120, 60, 60))
        pos = (panel_x + 120, w_h // 2 + 160)
        self.text_draw(str(player2_score), pos, "black")

    def draw_result(self, g_type, play_order, text):
        panel_x = self.panel_x
        w_h = self.w_h

        pygame.draw.rect(self.screen, self.get_color("white"), (panel_x - 120, w_h - self.font_size * 4 + 10, 600, self.font_size * 2))

        loc_text = (panel_x + 120, w_h - self.font_size * 3 + 10)
        if text == "DRAW":
            self.text_draw("DRAW", loc_text, "green")
            return None

        if g_type == "PvP":
            if play_order:
                self.text_draw(f"Player1 {text}", loc_text, "green")
            else:
                self.text_draw(f"Player2 {text}", loc_text, "green")

        elif g_type == "PvC":
            if play_order:
                self.text_draw(f"Player {text}", loc_text, "green")
            else:
                self.text_draw(f"Computer {text}", loc_text, "green")

    def draw_timer(self, turn_start_time, play_order):
        panel_x = self.panel_x
        w_h = self.w_h
        
        pygame.draw.rect(self.screen, self.get_color("white"), (panel_x - 100, w_h // 2 + 180, 400, self.button_size))
        pos = (panel_x + 120, w_h // 2 + 200)
        self.text_draw(f"Processed Time: {turn_start_time:.3f} s", pos, "blue")