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
from thegame    import TheGame



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

def main():
    def Update():
        display_surface.fill(white)
        display_surface.blit(game.level.surface,(0,0))
        display_surface.blit(grid,(0,0))
        display_surface.blit(game.overlay,(0,0))

        #temp code
        display_surface.blit(over,(0,0))
        mouse_check(game.matrix)
        mouse_check(game.inventory)
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
                        game.load_level()
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
    game.load_level()
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

def mouse_check(matrix):
    pos=pygame.mouse.get_pos()
    for row in matrix:
        for cell in row:
            if cell.collidepoint(pos):
                on_hover(cell)
                return cell

def on_hover(rect):
    Surface=pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
    pygame.draw.rect(Surface,(255,255,255,100),(0,0,rect.width,rect.height),border_radius=20)
    pygame.draw.rect(Surface,(0,200,200,50),(0,0,rect.width,rect.height),width=5,border_radius=20)
    display_surface.blit(Surface,rect.topleft)
    del Surface




over = pygame.Surface((1920,1080),pygame.SRCALPHA)
weapons_word = Goldie.render("Weapons",True,black)
characters_word = Goldie.render("Characters",True,black)
over.blit(characters_word,(30,60))
over.blit(weapons_word,(1590,60))


def Draw_grid(surface):
    size=60
    x=0
    y=0
    #verticle
    pygame.draw.circle(surface,red,(960,540),5)
    for i in range(32):
        pygame.draw.line(surface, black, (size*i+x,0),(size*i+x,1080), 1)
        surface.blit(NixieOne_small.render(str(size*i),True,red),(size*i,30))
    for i in range(18):
        pygame.draw.line(surface, black, (0,size*i+y),(1920,size*i+y),1)

grid =pygame.Surface((1920,1080),pygame.SRCALPHA)
#Draw_grid(grid)


#experimental code end.

if __name__ == '__main__':
    main()