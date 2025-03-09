import pygame

class Button:
    def __init__(self, screen, setting):
        self.screen = screen
        self.setting = setting
        self.SIZE = self.setting.button_size
        self.COL = self.setting.COL
        self.w_h = self.setting.w_h
        self.w, self.h = self.SIZE * 3, self.SIZE

    def button_is_hover(self, loc):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return loc[0] <= mouse_x <= loc[0] + self.w and loc[1] <= mouse_y <= loc[1] + self.h

    def button_draw(self, loc, pos, text, hover_text, text_draw):
        get_color = self.setting.get_color
        if self.button_is_hover(loc):
            pygame.draw.rect(self.screen, get_color("button_hover"), (loc[0], loc[1], self.w, self.h))
            text_draw(text, pos, "btn_text_hover")
        else:
            pygame.draw.rect(self.screen, get_color("button"), (loc[0], loc[1], self.w, self.h))
            text_draw(hover_text, pos, "btn_text")

    def draw_button(self, status, text_draw):
        shift_x = self.SIZE * 13 // 9   
        shift_y = self.SIZE // 2

        width, height = self.screen.get_size()
        self.x = width // 2 - self.SIZE * 3 // 2 if status is None else width - self.SIZE * 4
        self.y = height // 2 - self.SIZE * 5 // 4 if status is None else self.SIZE * 2

        if status is None:
            loc = (self.x, self.y)
            pos = (self.x + shift_x, loc[1] + shift_y)
            self.button_draw(loc, pos, "START", "PvP", text_draw)

            loc = (self.x, self.y + self.SIZE * 2)
            pos = (self.x + shift_x, loc[1] + shift_y)
            self.button_draw(loc, pos, "Computer", "Medium", text_draw)

            loc = (self.x - self.w - self.SIZE, self.y + self.SIZE * 2)
            pos = (loc[0] + shift_x, loc[1] + shift_y)
            self.button_draw(loc, pos, "Computer", "Easy", text_draw)

            loc = (self.x + self.w + self.SIZE, self.y + self.SIZE * 2)
            pos = (loc[0] + shift_x, loc[1] + shift_y)
            self.button_draw(loc, pos, "Computer", "Hard", text_draw)

        else:
            quit_loc = (self.x, self.w_h - self.SIZE)
            quit_text_y = quit_loc[1] + (self.h // 2) - (shift_y // 2) + (self.SIZE // 4)
            quit_pos = (self.x + shift_x, quit_text_y)
            self.button_draw(quit_loc, quit_pos, "QUIT", "QUIT", text_draw)

    def click_button(self, status):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if status is None:
            if self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h:
                if pygame.mouse.get_pressed()[0]:
                    return "start_pvp"

            if self.x <= mouse_x <= self.x + self.w and self.y + self.SIZE * 2 <= mouse_y <= self.y + self.SIZE * 2 + self.h:
                if pygame.mouse.get_pressed()[0]:
                    return "start_pvc_medium"

            easy_loc = (self.x - self.w - self.SIZE, self.y + self.SIZE * 2)
            if easy_loc[0] <= mouse_x <= easy_loc[0] + self.w and easy_loc[1] <= mouse_y <= easy_loc[1] + self.h:
                if pygame.mouse.get_pressed()[0]:
                    return "start_pvc_easy"

            hard_loc = (self.x + self.w + self.SIZE, self.y + self.SIZE * 2)
            if hard_loc[0] <= mouse_x <= hard_loc[0] + self.w and hard_loc[1] <= mouse_y <= hard_loc[1] + self.h:
                if pygame.mouse.get_pressed()[0]:
                    return "start_pvc_hard"

        else:
            if self.x <= mouse_x <= self.x + self.w and self.w_h - self.SIZE <= mouse_y <= self.w_h - self.SIZE + self.h:
                if pygame.mouse.get_pressed()[0]:
                    return "quit"

        return None