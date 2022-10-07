import pygame
import screeninfo
import sys
import math
import os
from colors     import *
from fonts      import *
from animations import Still
from animations import Animation
from levels     import Level
from characters import Character
from weapons    import Weapon



#initializations
pygame.init()
pygame.joystick.init()
screen          = screeninfo.get_monitors()[0]
joysticks       = [pygame.joystick.Joystick(i)for i in range(pygame.joystick.get_count())]
width, height   = screen.width, screen.height
clock           = pygame.time.Clock()
display_surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption('TheGame')

#global variables
inputs      = {'w':'up','a':'left','s':'down','d':'right','q':'no','e':'yes'}
directions = {pygame.K_UP:'up',pygame.K_LEFT:'left',pygame.K_DOWN:'down',pygame.K_RIGHT:'right'}
hat_directions={'(0, -1)':"up",'(0, 1)':'down','(1, 0)':'right','(-1, 0)':'left'}
move = {"up":[0,-1],"down":[0,1],"left":[-1,0],"right":[1,0]}

class TheGame():
    def __init__(self):
        self.state = 'weapon_place'
        self.characters=[Character('assets/Captain')]
        self.player = self.characters[0]
        self.level = Level()
        self.buffer= []

    def state_manager(self):
        pass
    def menu(self):
        pass
    def character_select(self):
        pass
    def weapon_select(self):
        pass
    def weapon_place(self):
        pass
    def run_phase(self):
        pass
    def result(self):
        pass
    def input_receive(self,direction,state):
        if state=='remove':
            if direction in self.buffer:
                self.buffer.remove(direction)
        elif state=='walk':
            if direction in self.buffer:
                print("Error_1")
            self.buffer.append(direction)
            if self.player.wait==0:
                self.set_wait()
                self.player.direction=direction
                self.player.idle(change=True)

    def set_wait(self):
        if self.buffer:
            while self.buffer:
                entry=self.buffer[-1]
                if self.player.position[1]+move[entry][0] in range(self.level.w):
                    if self.player.position[0]+move[entry][1] in range(self.level.h):
                        if self.player.direction!=entry:
                            self.player.direction=entry
                            self.player.idle(change=True)
                        else:
                            self.player.idle()
                        self.player.wait = 60
                        self.player.state='walk'
                        return
                    else:
                        self.buffer.remove(entry)
                else:
                    self.buffer.remove(entry)
                        

        if not self.buffer:
            self.player.wait=0
            self.state='idle'



def main():
    def Update():
        display_surface.fill(white)
        display_surface.blit(game.level.surface,(0,0))
        display_surface.blit(grid,(0,0))
        display_surface.blit(over,(0,0))

        #temp code
        mouse_check()
        game.player.SG.draw(display_surface)

        if game.player.state=='walk':
            if game.player.wait>0:
                game.player.walk()
                game.player.wait-=1
                if game.player.wait==0:
                    game.player.position[1]+=move[game.player.direction][0]
                    game.player.position[0]+=move[game.player.direction][1]
                    game.set_wait()

        #end temp code

    def Event_handler():
        events=pygame.event.get()
        if  events : 
            for event in events :
                #print(event)
                if event.type == pygame.KEYDOWN:
                    if event.key ==pygame.K_ESCAPE:
                        Quit()
                    elif event.unicode in inputs:
                        game.input_receive(inputs[event.unicode],'walk')
                    elif event.unicode=='p':
                        #use this for testing
                        game.level.next()
                        game.level.level_2()
                        game.player.position[0]+=1
                        game.player.position[1]+=1
                elif event.type == pygame.KEYUP:
                    if event.unicode in inputs:
                        game.input_receive(inputs[event.unicode],'remove')
                elif event.type == pygame.JOYBUTTONDOWN:
                    print(event)
                elif event.type == pygame.JOYBUTTONUP:
                    print(event)
                elif event.type == pygame.JOYHATMOTION:
                    if event.value[0]==1:
                        game.input_receive('right','walk')
                    elif event.value[0]==-1:
                        game.input_receive('left','walk')
                    elif event.value[1]==1:
                        game.input_receive('up','walk')
                    elif event.value[1]==-1:
                        game.input_receive('down','walk')
                    else:
                        game.input_receive(game.player.direction,'idle')
                elif event.type == pygame.QUIT:
                    Quit()
                        
            del events
            

    #code start : below this line

    game  = TheGame()
    game.level.occupants[2][0]='P1'
    game.player.position=[2,0]

    #code end : above this line
    while True:
        Update()
        Event_handler()
        pygame.display.update()
        clock.tick(60)

def Quit():
    pygame.quit()
    sys.exit()

#experimental code starts :

def on_hover(rect):
    Surface=pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
    Surface.fill((255,255,255,100))
    display_surface.blit(Surface,rect.topleft)
    del Surface

def blocks():
    size=60
    x,y,w,h=7,4,18,9
    for i in range(h):
        temp=[]
        for j in range(w):
            temp.append(pygame.Rect((x+j)*size,(y+i)*size,size,size))
            pygame.draw.rect(over,(255,255,255,20),((x+j)*size,(y+i)*size,size-3,size-3))
        matrix.append(temp)

matrix=[]
over = pygame.Surface((1920,1080),pygame.SRCALPHA)
blocks()
mine=Still('assets/weapon/bomb.png')
mine.resize(50,50)
weapons = NixieOne.render("Weapons",True,black)
Characters = NixieOne.render("Characters",True,black)


def mouse_check():
    pos=pygame.mouse.get_pos()
    for row in matrix:
        for cell in row:
            if cell.collidepoint(pos):
                on_hover(cell)
                #display_surface.blit(mine.image,cell.topleft)
                return cell

def Draw_grid(surface):
    size=60
    x=0
    y=0
    #verticle
    pygame.draw.circle(surface,red,(960,540),5)
    for i in range(32):
        pygame.draw.line(surface, black, (size*i+x,0),(size*i+x,1080), 1)
    for i in range(18):
        pygame.draw.line(surface, black, (0,size*i+y),(1920,size*i+y),1)

grid =pygame.Surface((1920,1080),pygame.SRCALPHA)
#Draw_grid(grid)


#experimental code end.

if __name__ == '__main__':
    main()