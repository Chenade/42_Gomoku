import pygame

class Config:
    def __init__(self):
        self.COL = 19
        self.SIZE = 80
        self.w_h = self.SIZE * (self.COL )

    def setup(self, title):
        
        pygame.display.set_caption(title)

        self.COL = 19
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # Make the window resizable
        self.w, self.h = self.screen.get_size()
        h = self.h
        self.screen = pygame.display.set_mode((h * 5 // 4, h * 5 // 6 ))
        self.SIZE = h // (self.COL + 5)
        self.w_h = self.SIZE * (self.COL)
        self.title = title
        self.screen.fill(self.palette("board"))

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

