import pygame
from animations import Animation
class Character():
    
    def __init__(self,path):
        self.animation = Animation(path)
        self.animation.zoom(1.5)
        self.animation.current_sprite = 0
        self.cycle_begin = 0
        self.cycle_end = 0
        self.SG = pygame.sprite.Group()
        self.SG.add(self.animation)
        self.animation.rect.center = (690,470)
        self.animation.current_sprite = 27
        self.cycle_begin = 27
        self.cycle_end = 36
        self.direction = "right"
        self.state = 'idle'
        self.wait = 0
        self.animation.play_animation=True
        self.animation.update(0.2)
        self.position=[0,0]

    def walk(self,change=False,speed=0.3,displace=1):
        move = {"up":[0,-1],"down":[0,1],"left":[-1,0],"right":[1,0]}
        self.animation.current_sprite += speed
        if int(self.animation.current_sprite) >= self.cycle_end:
            self.animation.current_sprite = self.cycle_begin
        self.animation.image = self.animation.sprites[int(self.animation.current_sprite)]
        self.animation.rect.center=(self.animation.rect.center[0]+move[self.direction][0]*displace,self.animation.rect.center[1]+move[self.direction][1]*displace)
    
    def idle(self,change=False):
        if change:
            if(self.direction=="up"):
                self.animation.current_sprite = 1
                self.cycle_begin = 1
                self.cycle_end=9
            elif(self.direction=="left"):
                self.animation.current_sprite = 9
                self.cycle_begin = 9
                self.cycle_end = 18
            elif(self.direction=="down"):
                self.animation.current_sprite = 19
                self.cycle_begin = 19
                self.cycle_end = 27
            elif(self.direction=="right"):
                self.animation.current_sprite = 27
                self.cycle_begin = 27
                self.cycle_end = 36
        self.animation.update(0.2)

