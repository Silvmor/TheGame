import pygame
from animations import Animation
class Character():
    
    def __init__(self,name):
        represent={'Captain':'P1','Spy':'P2'}
        self.name=name
        self.id=represent[name]
        self.animation = Animation('assets/'+name)
        self.animation.zoom(1.5)
        self.animation.play_animation=True
        self.SG = pygame.sprite.Group()
        self.SG.add(self.animation)
        self.animation.rect.center = (690,470)
        self.direction = 'right'
        self.state = 'idle'
        self.wait = 0
        self.idle(change=True)
        self.position=[0,0]
        self.HP = 3
        self.reveals=3
        self.took='free'
        eval('self.'+name+'()')

    def walk(self,change=False,speed=0.3,displace=1):
        #do something with move here self.direction=[0,0]
        move = {"up":[0,-1],"down":[0,1],"left":[-1,0],"right":[1,0]}
        self.animation.current_sprite += speed
        if int(self.animation.current_sprite) > self.cycle_end:
            self.animation.current_sprite = self.cycle_begin
        self.animation.image = self.animation.sprites[int(self.animation.current_sprite)]
        self.animation.rect.center=(self.animation.rect.center[0]+move[self.direction][0]*displace,self.animation.rect.center[1]+move[self.direction][1]*displace)
    
    def idle(self,change=False):
        if change:
            if(self.direction=="up"):
                self.animation.current_sprite = 1
                self.cycle_begin = 1
                self.cycle_end=8
            elif(self.direction=="left"):
                self.animation.current_sprite = 9
                self.cycle_begin = 9
                self.cycle_end = 17
            elif(self.direction=="down"):
                self.animation.current_sprite = 18
                self.cycle_begin = 18
                self.cycle_end = 26
            elif(self.direction=="right"):
                self.animation.current_sprite = 28
                self.cycle_begin = 28
                self.cycle_end = 35
        self.animation.update(0.2)

    def Captain(self):
        self.HP=4
    def Spy(self):
        self.reveals=4
