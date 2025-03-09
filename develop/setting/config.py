import pygame

class Config:
    def __init__(self,  title):
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # Make the window resizable
        self.w, self.h = self.screen.get_size()
        self.screen = pygame.display.set_mode((self.h * 5 // 4, self.h * 5 // 6 ))

        pygame.display.set_caption(title)
        self.title = title
        self.CAPTURE = 10
        self.set_column(19)


    def set_column(self, COL):
        self.COL = COL
        self.SIZE = self.h // (self.COL + 5)
        self.w_h = self.SIZE * (self.COL)
        self.screen.fill(self.palette("board"))
        self.panel_x = self.SIZE * (self.COL + 3)

    def get_color(self, color):
        return self.palette(color)

    def palette(self, color):
        if color == "black":
            return (0, 0, 0)
        elif color == "_black":
            return (50, 50, 50)
        elif color == "white":
            return (255, 255, 255)
        elif color == "_white":
            return (200, 200, 200)
        elif color == "red":
            return (255, 0, 0)
        elif color == "green":
            return (0, 200, 0)
        elif color == "gray":
            return (100, 100, 100)
        elif color == "board":
            return (255, 180, 0)
        elif color == "button":
            return (255, 255, 0)
        elif color == "ac_button":
            return (200, 200, 0)
        elif color == "btn_text":
            return (200, 0, 200)
        elif color == "btn_text_hover":
            return (255, 0, 255)
        else:
            return (0, 0, 0)

