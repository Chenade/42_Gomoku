import pygame

class Config:
    def __init__(self, title):
        self.color_options = ["black", "white", "red", "green", "gray", "yellow", "dark_green", "blue", "purple", "orange"]
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # Make the window resizable
        self.w, self.h = self.screen.get_size()
        self.screen = pygame.display.set_mode((self.h * 5 // 4, self.h * 5 // 6 ))

        pygame.display.set_caption(title)
        self.title = title
        self.CAPTURE = 10

        self.board_color = "yellow"
        self.line_color = "black"
        self.player1_color = "black"
        self.player2_color = "white"

        self.set_column(19)

    def set_column(self, COL):
        self.COL = COL
        self.SIZE = self.h // (self.COL + 5)
        self.w_h = self.SIZE * (self.COL)
        self.screen.fill(self.get_color(self.board_color))
        self.panel_x = self.SIZE * (self.COL + 3)

    def set_color(self, board_color=None, line_color=None, player1_color=None, player2_color=None):
        if board_color is not None and board_color in self.color_options:
            self.board_color = board_color
        if line_color is not None and line_color in self.color_options:
            self.line_color = line_color
        if player1_color is not None and player1_color in self.color_options:
            self.player1_color = player1_color
        if player2_color is not None and player2_color in self.color_options:
            self.player2_color = player2_color

    def get_color(self, color):
        if color == "board":
            return self.palette(self.board_color)
        elif color == "line":
            return self.palette(self.line_color)
        elif color == "player1":
            return self.palette(self.player1_color)
        elif color == "player2":
            return self.palette(self.player2_color)
        elif color == "hint":
            return self.palette("gray")
        elif color == "button":
            return (255, 255, 0)
        elif color == "button_hover":
            return (200, 200, 0)
        elif color == "btn_text":
            return (200, 0, 200)
        elif color == "btn_text_hover":
            return (255, 0, 255)
        else:
            return self.palette(color)

    def palette(self, color):
        if color == "black":
            return (0, 0, 0)
        elif color == "white":
            return (255, 255, 255)
        elif color == "red":
            return (255, 0, 0)
        elif color == "green":
            return (0, 200, 0)
        elif color == "gray":
            return (100, 100, 100)
        elif color == "yellow":
            return (255, 180, 0)
        elif color == "dark_green":
            return (0, 100, 0)
        elif color == "blue":
            return (0, 0, 255)
        elif color == "purple":
            return (128, 0, 128)
        elif color == "orange":
            return (255, 165, 0)
        else:
            print(color)
            return (0, 0, 0)

