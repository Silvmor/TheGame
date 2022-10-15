import pygame
import os


class Explosion:
    '''Class that animates the explosion when a character steps on weapon'''
    def __init__(self):
        self.original = []
        num = 0
        for img in os.listdir("assets/Explosion"):
            self.original.append(
                pygame.image.load(
                    "assets/Explosion/" + str(num) + ".png"
                ).convert_alpha()
            )
            num = num + 1

        self.sprites = self.original.copy()
        self.total_sprites = len(self.original)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 0
        self.zoom(0.5)

    def zoom(self, fact=1):
        '''Zooms the explosion'''
        (x, y) = self.rect.center
        width, height = int(self.rect.width * fact), int(self.rect.height * fact)
        self.sprites = self.original.copy()
        for slide in range(len(self.sprites)):
            self.sprites[slide] = pygame.transform.smoothscale(
                self.sprites[slide], (width, height)
            )
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.sprites[0].get_rect()
        self.rect.center = (x, y)

    def explode(self):
        '''Animates the explosion'''
        self.current_sprite += 0.2
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
