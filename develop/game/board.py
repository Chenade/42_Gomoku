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
                self.text_draw("PLAYER 1",self.panel_x + 120, self.w_h // 2 - 100, self.setting.palette("red"), SIZE // 2)
                self.text_draw("PLAYER 2",self.panel_x + 120, self.w_h // 2 + 100, self.setting.palette("black"), SIZE // 2)
            elif not play_order:
                self.text_draw("PLAYER 1",self.panel_x + 120, self.w_h // 2 - 100, self.setting.palette("black"), SIZE // 2)
                self.text_draw("PLAYER 2",self.panel_x + 120, self.w_h // 2 + 100, self.setting.palette("red"), SIZE // 2)
        else:
            if play_order:
                self.text_draw("PLAYER",self.panel_x + 120, self.w_h // 2 - 100, self.setting.palette("red"), SIZE // 2)
                self.text_draw("COMPUTER",self.panel_x + 120, self.w_h // 2 + 100, self.setting.palette("black"), SIZE // 2)
            elif not play_order:
                self.text_draw("PLAYER",self.panel_x + 120, self.w_h // 2 - 100, self.setting.palette("black"), SIZE // 2)
                self.text_draw("COMPUTER",self.panel_x + 120, self.w_h // 2 + 100, self.setting.palette("red"), SIZE // 2)
            
    def draw_score(self, player1_score, player2_score):
        self.player1_score, self.player2_score = player1_score, player2_score
        pygame.draw.circle(self.screen, self.setting.palette("black"), (self.panel_x, self.w_h // 2 - 50), SIZE // 5)
        self.text_draw(str(self.player1_score),self.panel_x + 120, self.w_h // 2 - 40, (100, 100, 100), SIZE)
        pygame.draw.circle(self.screen, self.setting.palette("white"), (self.panel_x, self.w_h // 2 + 150), SIZE//5)
        self.text_draw(str(self.player2_score),self.panel_x + 120, self.w_h // 2 + 160, self.setting.palette("black"), SIZE)

    def click_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        loc = (self.x, self.y + self.SIZE)
        if self.w + self.x > mouse_x > self.x and self.y + self.h > mouse_y > self.y:
            return "start_pvp"

        if self.w + self.x > mouse_x > self.x and self.y + self.SIZE * 2 + self.h > mouse_y > self.y + self.SIZE * 2:
            return "start_pvc"

        if self.w + self.x > mouse_x > self.x and self.w_h - 90 + self.h > mouse_y > self.w_h - 90:
            return "quit"

    def draw_title(self, play_order):
        #  _____               _       
        # |   __|___ _____ ___| |_ _ _ 
        # |  |  | . |     | . | '_| | |
        # |_____|___|_|_|_|___|_,_|___|
        if play_order is not None:
            self.text_draw("GOMOKU", self.panel_x + 120, SIZE, self.setting.palette("black"), SIZE)
        else:
            # draw text
            font = pygame.font.Font(None, self.SIZE * 2)
            text = font.render("GOMOKU", True, self.setting.palette("black"))
            width, height = self.screen.get_size()

            text_rect = text.get_rect(center=(width // 2, height // 2 - SIZE * 3))
            self.screen.blit(text, text_rect)

    def draw_button(self, play_order=None):
        shift_x = self.SIZE * 13 // 9   
        shift_y = self.SIZE // 2

        width, height = self.screen.get_size()
        self.x = width // 2 - self.SIZE * 3 // 2 if (play_order is None) else self.panel_x
        self.y = height // 2 - self.SIZE * 5 // 4 if (play_order is None) else self.SIZE * 2
        self.w, self.h = self.SIZE * 3, self.SIZE

        if play_order is None:
            # Play against player.
            loc = (self.x, self.y)
            pygame.draw.rect(self.screen, self.setting.palette("button"), (loc[0], loc[1], self.w, self.h))
            self.text_draw("PvP", self.x + shift_x, loc[1] + shift_y, self.setting.palette("red"), self.COL * 2)
            if self.click_button() == "start_pvp":
                pygame.draw.rect(self.screen, self.setting.palette("ac_button"), (loc[0], loc[1], self.w, self.h))
                self.text_draw("START", self.x + shift_x, loc[1] + shift_y, self.setting.palette("green"), self.COL * 2)

            # Play against computer.
            loc = (self.x, self.y + SIZE * 2)
            pygame.draw.rect(self.screen, self.setting.palette("button"), (loc[0], loc[1] , self.w, self.h))
            self.text_draw("COMPUTER", self.x + shift_x, loc[1] + shift_y, self.setting.palette("red"), self.COL * 2)
            if self.click_button() == "start_pvc":
                pygame.draw.rect(self.screen, self.setting.palette("ac_button"), (loc[0], loc[1], self.w, self.h))
                self.text_draw("START", self.x + shift_x, loc[1] + shift_y, self.setting.palette("green"), self.COL * 2)
        else:
            # Quit.
            pygame.draw.rect(self.screen, self.setting.palette("button"), (self.x, self.w_h - 90, self.w, self.h))
            self.text_draw("QUIT", self.x + shift_x, self.w_h - shift_y, self.setting.palette("btn_text"), self.COL * 2)
            if self.click_button() == "quit":
                pygame.draw.rect(self.screen, self.setting.palette("ac_button"), (self.x, self.w_h - 90, self.w, self.h))
                self.text_draw("Restart", self.x + shift_x, self.w_h - shift_y, self.setting.palette("btn_text_hover"), self.COL * 2)

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

        if text == "DRAW":
            self.text_draw("DRAW", self.panel_x + 100, self.w_h - self.SIZE * 4, self.setting.palette("green"), self.SIZE)
            return None

        if g_type == "PvP":
            if play_order == False:
                self.text_draw(f"Player1 {text}", self.panel_x + 100, self.w_h - self.SIZE * 4, self.setting.palette("green"), self.SIZE)
            elif play_order == True:
                self.text_draw(f"Player2 {text}", self.panel_x + 100, self.w_h - self.SIZE * 4, self.setting.palette("green"), self.SIZE)  

        elif g_type == "PvC":
            if play_order == False:
                self.text_draw(f"Player {text}", self.panel_x + 100, self.w_h - self.SIZE * 4, self.setting.palette("green"), self.SIZE)
            elif play_order == True:
                self.text_draw(f"Computer {text}", self.panel_x + 150, self.w_h - self.SIZE * 4, self.setting.palette("green"), self.SIZE - 10)
    
    def draw_timer(self, turn_start_time, play_order):
        timer_area = pygame.Rect(self.panel_x + 10, self.y + self.SIZE * 4, 200, 50) 
        pygame.draw.rect(self.screen, self.setting.palette("white"), timer_area)
        elapsed_time = (pygame.time.get_ticks() - turn_start_time)
        self.text_draw(f"Timer: {elapsed_time / 1000:.1f}s", self.panel_x + 110,  self.y + self.SIZE * 4 + 30, self.setting.palette("blue"), 30)
