import pygame
import screeninfo
import sys
import math
from colors import *
#from fonts import *
from animations import Animation
from animations import Still
import FakeServer


#initializations
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i)for i in range(pygame.joystick.get_count())]
joystick = pygame.joystick.Joystick(0)
screen_id       = 0
screen          = screeninfo.get_monitors()[screen_id]
width, height   = screen.width, screen.height
clock           = pygame.time.Clock()
display_surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption('TheGame')

#global variables
mouse_x,mouse_y=0,0
direction   = {'w':'up','a':'left','s':'down','d':'right'}
direction_2 = {pygame.K_UP:'up',pygame.K_LEFT:'left',pygame.K_DOWN:'down',pygame.K_RIGHT:'right'}
move        = {"up":[0,-1],"down":[0,1],"left":[-1,0],"right":[1,0]}


print(joysticks)




class Character():
    def __init__(self,path):
        self.animation=Animation(path)
        self.animation.zoom(1.5)
        self.animation.play_animation=True
        self.animation.current_sprite = 27
        self.cycle_begin=19
        self.cycle_end=27
        self.SG =pygame.sprite.Group()
        self.SG.add(self.animation)
        self.animation.rect.center=(64,300)
        self.direction="down"

    def walk(self,change=False,speed=0.3):
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
                self.animation.current_sprite = 28
                self.cycle_begin = 28
                self.cycle_end = 36
        self.animation.current_sprite += speed
        if int(self.animation.current_sprite) >= self.cycle_end:
            self.animation.current_sprite = self.cycle_begin
        self.animation.image = self.animation.sprites[int(self.animation.current_sprite)]
        
        self.animation.rect.center=(self.animation.rect.center[0]+move[self.direction][0],self.animation.rect.center[1]+move[self.direction][1])















#mainloop
Mover_group = pygame.sprite.Group()
Spy=Character("assets/Spy")
Captain=Character("assets/Captain")
Captain.animation.rect.center=(640,10)


Background_group = pygame.sprite.Group()
Back = Still('assets/level/level_1.png')
Ocean = Still('assets/level/Ocean.png')

Back.place(pos_x=1920/2,pos_y=1080/2,wrt='c')
#Back.place(pos_x=0,pos_y=-30)
Background_group.add(Ocean,Back)

Mover_group.add(Captain.animation)

def main() :
    
    while True:
        Update()
        Event_handler()
        pygame.display.update()
        clock.tick(60)        

def Event_handler():
    events=pygame.event.get()
    if  events : 
        for event in events :
            #print(event)
            if event.type == pygame.KEYDOWN :
                if event.unicode=='q' or event.key ==pygame.K_ESCAPE :
                    Quit()
                elif event.unicode in direction :
                    Captain.direction=direction[event.unicode]
                    Captain.walk(change=True)
                elif event.key == pygame.K_RETURN :
                    pass
            if event.type == pygame.JOYBUTTONDOWN :
                print(event)
            if event.type == pygame.JOYHATMOTION :
                print(event)
            elif event.type == pygame.MOUSEMOTION :
                mouse_x,mouse_y==event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame.QUIT :
                Quit()
                    
        del events
        
def Update():
    display_surface.fill(white)
    display_surface.blit(grid,(0,0))
    Spy.walk()
    Captain.walk()
    Mover_group.draw(display_surface)

def Quit():
    pygame.quit()
    sys.exit()

def Draw_grid(surface):
    size=60
    #x=20
    x=0
    y=0
    #verticle
    for i in range(32):
        pygame.draw.line(surface, black, (size*i+x,0),(size*i+x,1080), 1)
    for i in range(18):
        pygame.draw.line(surface, black, (0,size*i+y),(1920,size*i+y),1)
grid =pygame.Surface((1920,1080),pygame.SRCALPHA)
Draw_grid(grid)
Background_group.draw(grid)

main()