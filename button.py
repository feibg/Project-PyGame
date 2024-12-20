from settings import *

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, surface):
        if self.image != None:
            surface.blit(self.image, self.rect)
        surface.blit(self.text, self.text_rect)

    def input(self, pos):
        if pos[0] > self.rect.left and pos[0] < self.rect.right and pos[1] > self.rect.top and pos[1] < self.rect.bottom:
            return True
        return False

    def change_color(self, pos):
        if pos[0] > self.rect.left and pos[0] < self.rect.right and pos[1] > self.rect.top and pos[1] < self.rect.bottom:
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)