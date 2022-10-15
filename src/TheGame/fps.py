import pygame
from datetime import datetime
from colors import *
from fonts import *


class FPS:
    def __init__(self):
        self.FC = 60
        self.FPS = 60
        self.previous_time = datetime.now()
        self.current_time = datetime.now()
        self.font_color = black
        self.font = Courier
        self.view = self.font.render(str(self.FPS), True, self.font_color)
        self.rect = self.view.get_rect()
        self.rect.topleft = [0, 0]

    def show(self, surface):
        if self.FC == 0:
            self.FC = 60
            self.current_time = datetime.now()
            difference = self.current_time - self.previous_time
            difference /= 60
            time = datetime.strptime(str(difference), "%H:%M:%S.%f")
            self.FPS = int((1 / int(time.microsecond)) * 10 ** 6)
            self.previous_time = self.current_time
            del difference, time
        else:
            self.FC -= 1
        self.view = self.font.render(str(self.FPS), True, self.font_color)
        surface.blit(self.view, self.rect)
