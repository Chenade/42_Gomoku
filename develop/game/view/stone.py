import pygame

class Stone:
    def __init__(self, screen, setting):
        self.screen = screen
        self.SIZE = setting.SIZE
        self.COL = setting.COL
        self.get_color = setting.get_color

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
        loc = ((x_stone + 1) * self.SIZE, (y_stone + 1) * self.SIZE)
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