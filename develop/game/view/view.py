#  _____               _       
# |   __|___ _____ ___| |_ _ _ 
# |  |  | . |     | . | '_| | |
# |_____|___|_|_|_|___|_,_|___|

import pygame
from game.view import Button, Stone, Text


class View:
    def __init__(self, setting):
        self.update_setting(setting)
        self.get_color = setting.get_color
        self.player1_score = 0
        self.player2_score = 0

    def update_setting(self, setting):
        self.setting = setting
        self.screen = self.setting.screen
        self.COL = self.setting.COL
        self.SIZE = self.setting.SIZE
        self.w_h = self.setting.w_h
        self.panel_x = self.setting.panel_x
        self.button = Button(self.screen, setting)
        self.stone = Stone(self.screen, setting)
        self.text = Text(self.screen, setting)

    def draw_page(self, status):
        self.text.draw_title(status)
        self.button.draw_button(status, self.text.text_draw)

    def clean_page(self):
        self.screen.fill(self.get_color("board"))
        self.player1_score = 0
        self.player2_score = 0

    def draw_board(self, setting):
        self.update_setting(setting)
        self.screen.fill(self.get_color("board"))
        # Draw board
        for i in range(1, self.COL + 1):
            pygame.draw.line(self.screen, self.get_color("black"),
                             [self.SIZE * i, self.SIZE], [self.SIZE * i, self.w_h], 2)
            pygame.draw.line(self.screen, self.get_color("black"),
                             [self.SIZE, self.SIZE * i], [self.w_h, self.SIZE * i], 2)

    def text_player(self, g_type, play_order, player1_score, player2_score):
        self.text.draw_player(g_type, play_order, player1_score, player2_score)

    def text_result(self, g_type, play_order, text):
        self.text.draw_result(g_type, play_order, text)

    def text_timer(self, turn_start_time, play_order):
        self.text.draw_timer(turn_start_time, play_order)

    def click_button(self, status):
        return self.button.click_button(status)
   
    def get_stone_pos(self, _stones):
        return self.stone.get_stone_pos(_stones)

    def draw_stone(self, color, move):
        self.stone.draw_stone(color, move)

    def remove_stone(self, move):
        self.stone.remove_stone(move)

    def remove_captures(self, stones):
        self.stone.remove_captures(stones)

