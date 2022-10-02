#sprite creation class
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height,pos):
       super().__init__()
       self.image = pygame.Surface([width, height],pygame.SRCALPHA)
       self.image.fill(color)
       self.rect = self.image.get_rect()
       self.rect.center= pos