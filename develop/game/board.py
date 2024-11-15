import pygame

COL = 19
SIZE = 80

class Board:
    def __init__(self, setting):
        self.setting = setting
        self.w_h = SIZE * (COL)
        self.panel_x = SIZE * (COL + 2)
        self.screen = pygame.display.set_mode((2100, self.w_h + SIZE))
        self.screen.fill(self.setting.palette("board"))

    def draw_board(self, x=SIZE*COL + SIZE, y=SIZE, w=125, h=SIZE):
        self.screen.fill(self.setting.palette("board"))
        # Draw board
        for i in range(1, COL + 1):
            pygame.draw.line(self.screen, self.setting.palette("black"),
                             [SIZE * i, SIZE], [SIZE * i, self.w_h], 2)
            pygame.draw.line(self.screen, self.setting.palette("black"),
                             [SIZE, SIZE * i], [self.w_h, SIZE * i], 2)
        pygame.draw.circle(self.screen, self.setting.palette("black"), [SIZE * 8, SIZE * 8], 8)

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

        loc = (self.x, self.y + SIZE)
        if self.w + self.x > mouse_x > self.x and self.y + self.h > mouse_y > self.y:
            return "start_pvp"

        if self.w + self.x > mouse_x > self.x and self.y + SIZE * 2 + self.h > mouse_y > self.y + SIZE * 2:
            return "start_pvc"

        if self.w + self.x > mouse_x > self.x and self.w_h - 90 + self.h > mouse_y > self.w_h - 90:
            return "quit"

    def draw_title(self):
        #  _____               _       
        # |   __|___ _____ ___| |_ _ _ 
        # |  |  | . |     | . | '_| | |
        # |_____|___|_|_|_|___|_,_|___|
        self.text_draw("GOMOKU", self.panel_x + 120, SIZE, self.setting.palette("black"), SIZE)

    def draw_button(self, x=SIZE*COL, y=SIZE * 2, w=SIZE * 3, h=SIZE):
        self.x, self.y, self.w, self.h = self.panel_x, y, w, h
        self.button_color = self.setting.palette("button")
        self.ac_button_color = self.setting.palette("ac_button")

        # Play against player.
        loc = (self.x, self.y)
        pygame.draw.rect(self.screen, self.button_color, (loc[0], loc[1], w, h))
        self.text_draw("PvP", self.x + 120, loc[1] + 45, self.setting.palette("red"), COL * 2)
        if self.click_button() == "start_pvp":
            pygame.draw.rect(self.screen, self.ac_button_color, (loc[0], loc[1], self.w, self.h))
            self.text_draw("START", self.x + 120, loc[1] + 45, self.setting.palette("green"), COL * 2)

        # Play against computer.
        loc = (self.x, self.y + SIZE * 2)
        pygame.draw.rect(self.screen, self.button_color, (loc[0], loc[1] , w, h))
        self.text_draw("COMPUTER", self.x + 120, loc[1] + 45, self.setting.palette("red"), COL * 2)
        if self.click_button() == "start_pvc":
            pygame.draw.rect(self.screen, self.ac_button_color, (loc[0], loc[1], self.w, self.h))
            self.text_draw("START", self.x + 120, loc[1] + 45, self.setting.palette("green"), COL * 2)

        # Quit.
        pygame.draw.rect(self.screen, self.button_color, (self.x, self.w_h - 90, w, h))
        self.text_draw("QUIT", self.x + 120, self.w_h - 50, (200, 0, 200), COL * 2)
        if self.click_button() == "quit":
            pygame.draw.rect(self.screen, self.ac_button_color, (self.x, self.w_h - 90, self.w, self.h))
            self.text_draw("Quit", self.x + 120, self.w_h - 50, (225, 0, 225), COL * 2)

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

        if SIZE < x_stone < SIZE * COL and SIZE < y_stone < SIZE * COL:
            if x_stone % SIZE > SIZE // 2:
                x_stone = (x_stone - x_stone % SIZE) + SIZE
            else:
                x_stone -= x_stone % SIZE

            if y_stone % SIZE > SIZE // 2:
                y_stone = (y_stone - y_stone % SIZE) + SIZE
            else:
                y_stone -= y_stone % SIZE

            return x_stone // SIZE - 1, y_stone // SIZE - 1

        else:
            return None, None

    def draw_stone(self, play_order, x_stone, y_stone):
        if play_order:
            self.stone_color = self.setting.palette("black")
        else:
            self.stone_color = self.setting.palette("white")

        self.x_stone, self.y_stone = x_stone, y_stone
        loc = ((self.x_stone + 1) * SIZE, (self.y_stone + 1) * SIZE)
        pygame.draw.circle(self.screen, self.stone_color, loc, SIZE // 2)

    def draw_result(self, g_type, play_order, text):

        if text == "DRAW":
            self.text_draw("DRAW", self.panel_x + 100, self.w_h - SIZE * 4, self.setting.palette("green"), SIZE)
            return None

        if g_type == "PvP":
            if play_order == False:
                self.text_draw(f"Player1 {text}", self.panel_x + 100, self.w_h - SIZE * 4, self.setting.palette("green"), SIZE)
            elif play_order == True:
                self.text_draw(f"Player2 {text}", self.panel_x + 100, self.w_h - SIZE * 4, self.setting.palette("green"), SIZE)  

        elif g_type == "PvC":
            if play_order == False:
                self.text_draw(f"Player {text}", self.panel_x + 100, self.w_h - SIZE * 4, self.setting.palette("green"), SIZE)
            elif play_order == True:
                self.text_draw(f"Computer {text}", self.panel_x + 150, self.w_h - SIZE * 4, self.setting.palette("green"), SIZE - 10)
    
    def draw_timer(self, turn_start_time, play_order):
        timer_area = pygame.Rect(self.panel_x + 10, self.y + SIZE * 4, 200, 50) 
        pygame.draw.rect(self.screen, self.setting.palette("white"), timer_area)
        elapsed_time = (pygame.time.get_ticks() - turn_start_time)
        self.text_draw(f"Timer: {elapsed_time / 1000:.1f}s", self.panel_x + 110,  self.y + SIZE * 4 + 30, self.setting.palette("blue"), 30)
