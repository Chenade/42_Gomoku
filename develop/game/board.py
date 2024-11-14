import pygame

COL = 19
SIZE = 80

class Board:
    def __init__(self, setting):
        self.setting = setting
        self.w_h = SIZE * (COL + 1)
        self.panel_x = SIZE * (COL + 3)
        self.screen = pygame.display.set_mode((2100, self.w_h + SIZE))
        self.screen.fill(self.setting.palette("board"))

    def draw_board(self, x=SIZE*COL + SIZE, y=SIZE, w=125, h=SIZE):

        # Draw board
        for i in range(1, COL + 2):
            pygame.draw.line(self.screen, self.setting.palette("black"),
                             [SIZE * i, SIZE], [SIZE * i, self.w_h], 2)
            pygame.draw.line(self.screen, self.setting.palette("black"),
                             [SIZE, SIZE * i], [self.w_h, SIZE * i], 2)
        pygame.draw.circle(self.screen, self.setting.palette("black"), [SIZE * 8, SIZE * 8], 8)

    def draw_player(self, play_order):
        if play_order is None:
            self.text_draw("PLAYER 1",self.panel_x + 120, self.w_h // 2 - 100, (100, 100, 100), COL)
            self.text_draw("PLAYER 2",self.panel_x + 120, self.w_h // 2 + 100, self.setting.palette("black"), COL)
        elif play_order:
            self.text_draw("PLAYER 1",self.panel_x + 120, self.w_h // 2 - 100, self.setting.palette("red"), COL)
            self.text_draw("PLAYER 2",self.panel_x + 120, self.w_h // 2 + 100, self.setting.palette("black"), COL)
        elif not play_order:
            self.text_draw("PLAYER 1",self.panel_x + 120, self.w_h // 2 - 100, self.setting.palette("black"), COL)
            self.text_draw("PLAYER 2",self.panel_x + 120, self.w_h // 2 + 100, self.setting.palette("red"), COL)
            
    def draw_score(self, player1_score, player2_score):
        self.player1_score, self.player2_score = player1_score, player2_score
        pygame.draw.circle(self.screen, self.setting.palette("white"), (self.panel_x, self.w_h // 2 - 50), SIZE // 5)
        self.text_draw(str(self.player1_score),self.panel_x + 120, self.w_h // 2 - 40, (100, 100, 100), SIZE)
        pygame.draw.circle(self.screen, self.setting.palette("black"), (self.panel_x, self.w_h // 2 + 150), SIZE//5)
        self.text_draw(str(self.player2_score),self.panel_x + 120, self.w_h // 2 + 160, self.setting.palette("black"), SIZE)

    def draw_button(self, x=SIZE*COL, y=SIZE, w=SIZE * 3, h=SIZE):
        self.x, self.y, self.w, self.h = self.panel_x, y, w, h
        self.button_color = self.setting.palette("button")
        self.ac_button_color = self.setting.palette("ac_button")

        mouse = pygame.mouse.get_pos()

        # New game.
        pygame.draw.rect(self.screen, self.button_color, (self.x, self.y, w, h))
        self.text_draw("NEW GAME", self.x + 120, self.y + 40, (200, 0, 0), COL * 2)
        if self.w + self.x > mouse[0] > self.x and \
                self.y + self.h > mouse[1] > self.y:
            pygame.draw.rect(self.screen, self.ac_button_color, (self.x, self.y, self.w, self.h))
            self.text_draw("START", self.x + 120, self.y + 40, self.setting.palette("red"), COL * 2)

        # Quit.
        pygame.draw.rect(self.screen, self.button_color, (self.x, self.w_h - 90, w, h))
        self.text_draw("QUIT", self.x + 120, self.w_h - 50, (200, 0, 200), COL * 2)
        if self.w + self.x > mouse[0] > self.x and \
                self.w_h - 90 + self.h > mouse[1] > self.w_h - 90:
            pygame.draw.rect(self.screen, self.ac_button_color, (self.x, self.w_h - 90, self.w, self.h))
            self.text_draw("Quit", self.x + 120, self.w_h - 50, (225, 0, 225), COL * 2)
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.quit()
                quit()

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

    def get_pos(self):
        self.x_stone, self.y_stone = pygame.mouse.get_pos()

        return self.x_stone, self.y_stone

    def get_stone_pos(self):
        if self.x_stone % SIZE > SIZE // 2:
            self.x_stone = (self.x_stone - self.x_stone % SIZE) + SIZE
        else:
            self.x_stone -= self.x_stone % SIZE

        if self.y_stone % SIZE > SIZE // 2:
            self.y_stone = (self.y_stone - self.y_stone % SIZE) + SIZE
        else:
            self.y_stone -= self.y_stone % SIZE

        return self.x_stone, self.y_stone

    def draw_stone(self, stone, color_name, stone_color, x_stone, y_stone):
        self.stones, player_color = stone, color_name
        self.stone_color, self.x_stone, self.y_stone = stone_color, x_stone, y_stone

        # if (self.x_stone, self.y_stone) in self.stones["white"]:
        #     pass
        # elif (self.x_stone, self.y_stone) in self.stones["black"]:
        #     pass
        # else:
        pygame.draw.circle(self.screen, self.stone_color,(self.x_stone, self.y_stone), SIZE//2)
        self.stones[player_color].append((self.x_stone, self.y_stone))
        self._stones[x_stone, y_stone] = (color_name == "black") and 1 or 2

        return self.stones

    
    def draw_result(self, winner, text):
        if winner == "white":
            self.text_draw(text, self.panel_x - 20, self.w_h // 2 - 120, self.setting.palette("green"), SIZE)

        elif winner == "black":
            self.text_draw(text, self.panel_x - 20, self.w_h // 2 + 120, self.setting.palette("green"), SIZE)    

        return None