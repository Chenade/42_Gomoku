#  _____               _       
# |   __|___ _____ ___| |_ _ _ 
# |  |  | . |     | . | '_| | |
# |_____|___|_|_|_|___|_,_|___|

import pygame
from setting.config import Config

class Board:
    def __init__(self, setting):
        self.setting = setting
        self.screen = self.setting.screen
        self.COL = self.setting.COL
        self.SIZE = self.setting.SIZE
        self.w_h = self.setting.w_h
        self.panel_x = self.SIZE * (self.COL + 3)
        self.player1_score = 0
        self.player2_score = 0
    
    def get_color(self, color):
        return self.setting.palette(color)

    def text_draw(self, text, pos, font_color, font_size):
        x_pos, y_pos = pos
        self.text = text
        self.font_size = font_size
        self.font_color = self.get_color(font_color)
        ff = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        TextSurf, TextRect = self.text_objects(self.text, ff, self.font_color)
        TextRect.center = (x_pos, y_pos)
        self.screen.blit(TextSurf, TextRect)

    def text_objects(self, text, font, font_color):
        textSurface = font.render(text, True, font_color)
        return textSurface, textSurface.get_rect()

    def draw_title(self, game_type):
        if game_type is not None:
            pos = (self.panel_x + 120, self.SIZE)
            self.text_draw("GOMOKU", pos, "black", self.SIZE // 2)
            pos = (self.panel_x + 120, self.SIZE * 2)
            if game_type == "PvP":
                self.text_draw("Player against Player", pos, "green", self.SIZE // 3)
            elif game_type == "PvC":
                self.text_draw("Player against Computer", pos, "green", self.SIZE // 3)
        else:
            # draw text
            font = pygame.font.Font(None, self.SIZE * 2)
            text = font.render("GOMOKU", True, self.get_color("black"))
            width, height = self.screen.get_size()

            text_rect = text.get_rect(center=(width // 2, height // 2 - self.SIZE * 3))
            self.screen.blit(text, text_rect)

    def clean_board(self):
        self.screen.fill(self.get_color("board"))
        self.player1_score = 0
        self.player2_score = 0

    def draw_board(self):
        self.screen.fill(self.get_color("board"))
        # Draw board
        for i in range(1, self.COL + 1):
            pygame.draw.line(self.screen, self.get_color("black"),
                             [self.SIZE * i, self.SIZE], [self.SIZE * i, self.w_h], 2)
            pygame.draw.line(self.screen, self.get_color("black"),
                             [self.SIZE, self.SIZE * i], [self.w_h, self.SIZE * i], 2)

    def draw_player(self, g_type, play_order, player1_score, player2_score):
        pos_player_1 = (self.panel_x + 120, self.w_h // 2 - 100)
        pos_player_2 = (self.panel_x + 120, self.w_h // 2 + 100)
        if g_type == "PvP":
            if play_order:
                self.text_draw("PLAYER 1",pos_player_1, "red", self.SIZE // 3)
                self.text_draw("PLAYER 2",pos_player_2, "black", self.SIZE // 3)
            elif not play_order:
                self.text_draw("PLAYER 1",pos_player_1, "black", self.SIZE // 3)
                self.text_draw("PLAYER 2",pos_player_2, "red", self.SIZE // 3)
        else:
            if play_order:
                self.text_draw("PLAYER",pos_player_1, "red", self.SIZE // 3)
                self.text_draw("COMPUTER",pos_player_2, "black", self.SIZE // 3)
            elif not play_order:
                self.text_draw("PLAYER",pos_player_1, "black", self.SIZE // 3)
                self.text_draw("COMPUTER",pos_player_2, "red", self.SIZE // 3)

        pygame.draw.circle(self.screen, self.get_color("black"), (self.panel_x, self.w_h // 2 - 50), self.SIZE // 5)
        pygame.draw.circle(self.screen, self.get_color("white"), (self.panel_x, self.w_h // 2 + 150), self.SIZE//5)
        
        # Draw score
        if player1_score != self.player1_score or player1_score == 0:
            pygame.draw.rect(self.screen, self.get_color("board"), (self.panel_x + 70, self.w_h // 2 - 80 , 80, 80))
            pos = (self.panel_x + 120, self.w_h // 2 - 40)
            self.text_draw(str(player1_score), pos, "black", self.SIZE)
        
        if player2_score != self.player2_score or player2_score == 0:
            pygame.draw.rect(self.screen, self.get_color("board"), (self.panel_x + 90, self.w_h // 2 + 120 , 60, 60))
            pos = (self.panel_x + 120, self.w_h // 2 + 160)
            self.text_draw(str(player2_score), pos, "black", self.SIZE)
            
        self.player1_score, self.player2_score = player1_score, player2_score

    def click_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h:
            if pygame.mouse.get_pressed()[0]:
                return "start_pvp"

        if self.x <= mouse_x <= self.x + self.w and self.y + self.SIZE * 2 <= mouse_y <= self.y + self.SIZE * 2 + self.h:
            if pygame.mouse.get_pressed()[0]:
                return "start_pvc"

        if self.x <= mouse_x <= self.x + self.w and self.w_h - self.SIZE <= mouse_y <= self.w_h - self.SIZE + self.h:
            if pygame.mouse.get_pressed()[0]:
                return "quit"

        return None

    def draw_button(self, g_type=None):
        shift_x = self.SIZE * 13 // 9   
        shift_y = self.SIZE // 2

        width, height = self.screen.get_size()
        self.x = width // 2 - self.SIZE * 3 // 2 if g_type is None else width - self.SIZE * 4
        self.y = height // 2 - self.SIZE * 5 // 4 if g_type is None else self.SIZE * 2
        self.w, self.h = self.SIZE * 3, self.SIZE

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if g_type is None:
            loc = (self.x, self.y)
            pos = (self.x + shift_x, loc[1] + shift_y)
            if self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h:
                pygame.draw.rect(self.screen, self.get_color("ac_button"), (loc[0], loc[1], self.w, self.h))
                self.text_draw("START", pos, "green", self.COL)
            else:
                pygame.draw.rect(self.screen, self.get_color("button"), (loc[0], loc[1], self.w, self.h))
                self.text_draw("PvP", pos, "red", self.COL)

            loc = (self.x, self.y + self.SIZE * 2)
            pos = (self.x + shift_x, loc[1] + shift_y)
            if self.x <= mouse_x <= self.x + self.w and self.y + self.SIZE * 2 <= mouse_y <= self.y + self.SIZE * 2 + self.h:
                pygame.draw.rect(self.screen, self.get_color("ac_button"), (loc[0], loc[1], self.w, self.h))
                self.text_draw("START", pos, "green", self.COL)
            else:
                pygame.draw.rect(self.screen, self.get_color("button"), (loc[0], loc[1], self.w, self.h))
                self.text_draw("Computer", pos, "red", self.COL)

        else:
            quit_loc = (self.x, self.w_h - self.SIZE)
            quit_text_y = quit_loc[1] + (self.h // 2) - (shift_y // 2) + (self.SIZE // 4)
            quit_pos = (self.x + shift_x, quit_text_y)
            if self.x <= mouse_x <= self.x + self.w and self.w_h - self.SIZE <= mouse_y <= self.w_h - self.SIZE + self.h:
                pygame.draw.rect(self.screen, self.get_color("ac_button"), (quit_loc[0], quit_loc[1], self.w, self.h))
                self.text_draw("RESTART", quit_pos, "red", self.COL)
            else:
                pygame.draw.rect(self.screen, self.get_color("button"), (quit_loc[0], quit_loc[1], self.w, self.h))
                self.text_draw("MENU", quit_pos, "btn_text", self.COL)

    def get_stone_pos(self, _stones):
        y_stone, x_stone = pygame.mouse.get_pos()

        if self.SIZE < x_stone < self.SIZE * self.COL and self.SIZE < y_stone < self.SIZE * self.COL:

            if x_stone % self.SIZE > self.SIZE // 2:
                x_stone = (x_stone - x_stone % self.SIZE) + self.SIZE
            else:
                x_stone -= x_stone % self.SIZE

            if y_stone % self.SIZE > self.SIZE // 2:
                y_stone = (y_stone - y_stone % self.SIZE) + self.SIZE
            else:
                y_stone -= y_stone % self.SIZE

            if (_stones[x_stone // self.SIZE - 1][y_stone // self.SIZE - 1] != 0):
                return None

            return (x_stone // self.SIZE - 1, y_stone // self.SIZE - 1)

        else:
            return None

    def draw_stone(self, color, move):
        y_stone, x_stone = move
        stone_color = self.get_color(color)
        self.x_stone, self.y_stone = x_stone, y_stone
        loc = ((self.x_stone + 1) * self.SIZE, (self.y_stone + 1) * self.SIZE)
        pygame.draw.circle(self.screen, stone_color, loc, self.SIZE // 2)

    def remove_stone(self, move):
        y_stone, x_stone = move
        loc = ((x_stone + 1) * self.SIZE, (y_stone + 1) * self.SIZE)
        pygame.draw.circle(self.screen, self.get_color("board"), loc, self.SIZE // 2)
        pygame.draw.line(self.screen, self.get_color("black"),
                         [loc[0] - self.SIZE // 2, loc[1]], [loc[0] + self.SIZE // 2, loc[1]], 2)
        pygame.draw.line(self.screen, self.get_color("black"),
                            [loc[0], loc[1] - self.SIZE // 2], [loc[0], loc[1] + self.SIZE // 2], 2)

    def remove_captures(self, stones):
        for i in range(self.COL):
            for j in range(self.COL):
                if stones[i][j] == 3:
                    self.remove_stone((i, j))
                    stones[i][j] = 0

    def draw_result(self, g_type, play_order, text):
        pygame.draw.rect(self.screen, self.get_color("white"), (self.panel_x - 120, self.w_h - self.SIZE * 4, 600, self.SIZE * 2))
        
        loc_text = (self.panel_x + 120,  self.w_h - self.SIZE * 3)
        if text == "DRAW":
            self.text_draw("DRAW",loc_text, "green", self.SIZE)
            return None

        if g_type == "PvP":
            if play_order:
                self.text_draw(f"Player1 {text}",loc_text, "green", self.SIZE)
            else:
                self.text_draw(f"Player2 {text}",loc_text, "green", self.SIZE)  

        elif g_type == "PvC":
            if play_order:
                self.text_draw(f"Player {text}",loc_text, "green", self.SIZE)
            else:
                self.text_draw(f"Computer {text}", loc_text, "green", self.SIZE - 10)
            
    def draw_timer(self, turn_start_time, play_order):
        pygame.draw.rect(self.screen, self.get_color("white"), (self.panel_x - 100, self.w_h // 2 + 180 , 400, self.SIZE))
        pos = (self.panel_x + 120,  self.w_h // 2 + 200)
        self.text_draw(f"Processed Time: {turn_start_time:.3f} s", pos, "blue", self.SIZE // 3)
