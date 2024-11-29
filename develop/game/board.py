#  _____               _       
# |   __|___ _____ ___| |_ _ _ 
# |  |  | . |     | . | '_| | |
# |_____|___|_|_|_|___|_,_|___|

import pygame

COL = 19
SIZE = 80

class Board:
    def __init__(self, setting):
        self.setting = setting
        self.screen = self.setting.screen
        self.COL = self.setting.COL
        self.SIZE = self.setting.SIZE
        self.w_h = self.setting.w_h
        self.panel_x = self.SIZE * (self.COL + 3)

    def text_draw(self, text, x_pos, y_pos, font_color, font_size):
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        ff = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        TextSurf, TextRect = self.text_objects(self.text, ff, self.font_color)
        TextRect.center = (x_pos, y_pos)
        self.screen.blit(TextSurf, TextRect)

    def text_objects(self, text, font, font_color):
        textSurface = font.render(text, True, font_color)
        return textSurface, textSurface.get_rect()

    def draw_title(self, game_type):
        if game_type is not None:
            self.text_draw("GOMOKU", self.panel_x + 120, SIZE, self.setting.palette("black"), SIZE // 2)
            if game_type == "PvP":
                self.text_draw("Player against Player", self.panel_x + 120, SIZE * 2, self.setting.palette("green"), SIZE // 3)
            elif game_type == "PvC":
                self.text_draw("Player against Computer", self.panel_x + 120, SIZE * 2, self.setting.palette("green"), SIZE // 3)
        else:
            # draw text
            font = pygame.font.Font(None, self.SIZE * 2)
            text = font.render("GOMOKU", True, self.setting.palette("black"))
            width, height = self.screen.get_size()

            text_rect = text.get_rect(center=(width // 2, height // 2 - SIZE * 3))
            self.screen.blit(text, text_rect)

    def clean_board(self):
        self.screen.fill(self.setting.palette("board"))

    def draw_board(self):
        self.screen.fill(self.setting.palette("board"))
        # Draw board
        for i in range(1, COL + 1):
            pygame.draw.line(self.screen, self.setting.palette("black"),
                             [self.SIZE * i, self.SIZE], [self.SIZE * i, self.w_h], 2)
            pygame.draw.line(self.screen, self.setting.palette("black"),
                             [self.SIZE, self.SIZE * i], [self.w_h, self.SIZE * i], 2)

    def draw_player(self, g_type, play_order):
        if g_type == "PvP":
            if play_order:
                self.text_draw("PLAYER 1",self.panel_x + 120, self.w_h // 2 - 100, self.setting.palette("red"), SIZE // 3)
                self.text_draw("PLAYER 2",self.panel_x + 120, self.w_h // 2 + 100, self.setting.palette("black"), SIZE // 3)
            elif not play_order:
                self.text_draw("PLAYER 1",self.panel_x + 120, self.w_h // 2 - 100, self.setting.palette("black"), SIZE // 3)
                self.text_draw("PLAYER 2",self.panel_x + 120, self.w_h // 2 + 100, self.setting.palette("red"), SIZE // 3)
        else:
            if play_order:
                self.text_draw("PLAYER",self.panel_x + 120, self.w_h // 2 - 100, self.setting.palette("red"), SIZE // 3)
                self.text_draw("COMPUTER",self.panel_x + 120, self.w_h // 2 + 100, self.setting.palette("black"), SIZE // 3)
            elif not play_order:
                self.text_draw("PLAYER",self.panel_x + 120, self.w_h // 2 - 100, self.setting.palette("black"), SIZE // 3)
                self.text_draw("COMPUTER",self.panel_x + 120, self.w_h // 2 + 100, self.setting.palette("red"), SIZE // 3)
            
    def draw_score(self, player1_score, player2_score):
        self.player1_score, self.player2_score = player1_score, player2_score
        pygame.draw.circle(self.screen, self.setting.palette("black"), (self.panel_x, self.w_h // 2 - 50), SIZE // 5)
        self.text_draw(str(self.player1_score),self.panel_x + 120, self.w_h // 2 - 40, (100, 100, 100), SIZE)
        pygame.draw.circle(self.screen, self.setting.palette("white"), (self.panel_x, self.w_h // 2 + 150), SIZE//5)
        self.text_draw(str(self.player2_score),self.panel_x + 120, self.w_h // 2 + 150, self.setting.palette("black"), SIZE)

    def click_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Check for PvP button click
        if self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h:
            if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is clicked
                return "start_pvp"

        # Check for PVC button click
        if self.x <= mouse_x <= self.x + self.w and self.y + self.SIZE * 2 <= mouse_y <= self.y + self.SIZE * 2 + self.h:
            if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is clicked
                return "start_pvc"

        # Check for Quit button click
        if self.x <= mouse_x <= self.x + self.w and self.w_h - self.SIZE <= mouse_y <= self.w_h - self.SIZE + self.h:
            if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is clicked
                return "quit"

        return None  # No button clicked

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
            if self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h:
                pygame.draw.rect(self.screen, self.setting.palette("ac_button"), (loc[0], loc[1], self.w, self.h))
                self.text_draw("START", self.x + shift_x, loc[1] + shift_y, self.setting.palette("green"), self.COL)
            else:
                pygame.draw.rect(self.screen, self.setting.palette("button"), (loc[0], loc[1], self.w, self.h))
                self.text_draw("PvP", self.x + shift_x, loc[1] + shift_y, self.setting.palette("red"), self.COL)

            loc = (self.x, self.y + self.SIZE * 2)
            if self.x <= mouse_x <= self.x + self.w and self.y + self.SIZE * 2 <= mouse_y <= self.y + self.SIZE * 2 + self.h:
                pygame.draw.rect(self.screen, self.setting.palette("ac_button"), (loc[0], loc[1], self.w, self.h))
                self.text_draw("START", self.x + shift_x, loc[1] + shift_y, self.setting.palette("green"), self.COL)
            else:
                pygame.draw.rect(self.screen, self.setting.palette("button"), (loc[0], loc[1], self.w, self.h))
                self.text_draw("Computer", self.x + shift_x, loc[1] + shift_y, self.setting.palette("red"), self.COL)

        else:
            quit_loc = (self.x, self.w_h - self.SIZE)
            quit_text_y = quit_loc[1] + (self.h // 2) - (shift_y // 2) + (self.SIZE // 4)
            if self.x <= mouse_x <= self.x + self.w and self.w_h - self.SIZE <= mouse_y <= self.w_h - self.SIZE + self.h:
                pygame.draw.rect(self.screen, self.setting.palette("ac_button"), (quit_loc[0], quit_loc[1], self.w, self.h))
                self.text_draw("RESTART", self.x + shift_x, quit_text_y, self.setting.palette("red"), self.COL)
            else:
                pygame.draw.rect(self.screen, self.setting.palette("button"), (quit_loc[0], quit_loc[1], self.w, self.h))
                self.text_draw("MENU", self.x + shift_x, quit_text_y, self.setting.palette("btn_text"), self.COL)

    def get_stone_pos(self):

        x_stone, y_stone = pygame.mouse.get_pos()

        if self.SIZE < x_stone < self.SIZE * COL and self.SIZE < y_stone < self.SIZE * COL:
            if x_stone % self.SIZE > self.SIZE // 2:
                x_stone = (x_stone - x_stone % self.SIZE) + self.SIZE
            else:
                x_stone -= x_stone % self.SIZE

            if y_stone % self.SIZE > self.SIZE // 2:
                y_stone = (y_stone - y_stone % self.SIZE) + self.SIZE
            else:
                y_stone -= y_stone % self.SIZE

            return x_stone // self.SIZE - 1, y_stone // self.SIZE - 1

        else:
            return None, None

    def draw_stone(self, play_order, x_stone, y_stone):
        if play_order:
            self.stone_color = self.setting.palette("black")
        else:
            self.stone_color = self.setting.palette("white")

        self.x_stone, self.y_stone = x_stone, y_stone
        loc = ((self.x_stone + 1) * self.SIZE, (self.y_stone + 1) * self.SIZE)
        pygame.draw.circle(self.screen, self.stone_color, loc, self.SIZE // 2)

    def draw_result(self, g_type, play_order, text):
        pygame.draw.rect(self.screen, self.setting.palette("white"), ( self.w_h + 2, self.w_h - self.SIZE * 4, 500, self.SIZE * 2))
        
        loc_text = (self.panel_x + 100,  self.w_h - self.SIZE * 3)
        if text == "DRAW":
            self.text_draw("DRAW",loc_text[0], loc_text[1], self.setting.palette("green"), self.SIZE)
            return None

        if g_type == "PvP":
            if play_order == False:
                self.text_draw(f"Player1 {text}",loc_text[0], loc_text[1], self.setting.palette("green"), self.SIZE)
            elif play_order == True:
                self.text_draw(f"Player2 {text}",loc_text[0], loc_text[1], self.setting.palette("green"), self.SIZE)  

        elif g_type == "PvC":
            if play_order == False:
                self.text_draw(f"Computer {text}", loc_text[0], loc_text[1], self.setting.palette("green"), self.SIZE - 10)
            elif play_order == True:
                self.text_draw(f"Player {text}",loc_text[0], loc_text[1], self.setting.palette("green"), self.SIZE)
            
    def draw_timer(self, turn_start_time, play_order):
        pygame.draw.rect(self.screen, self.setting.palette("white"), (self.panel_x, self.w_h // 2 + 10 , 200, self.h))
        elapsed_time = (pygame.time.get_ticks() - turn_start_time)
        seconds = elapsed_time / 1000
        formatted_time = f"{seconds:.1f}".rjust(8)
        self.text_draw(f"Timer: {formatted_time} s", self.panel_x + 110,  self.w_h // 2 + 30, self.setting.palette("blue"), self.SIZE // 2)
