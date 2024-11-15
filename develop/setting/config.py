class Config:
    def __init__(self):
        self.COL = 19
        self.SIZE = 80
        self.w_h = self.SIZE * (self.COL + 1)

    def setup(self, title):
        self.title = title
        self.screen = pygame.display.set_mode((2100, self.w_h + self.SIZE))
        pygame.display.set_caption(self.title)
        self.screen.fill(self.palette("board"))

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
        elif color == "board":
            return (255, 180, 0)
        elif color == "button":
            return (255, 255, 0)
        elif color == "ac_button":
            return (200, 200, 0)
        else:
            return (0, 0, 0)

