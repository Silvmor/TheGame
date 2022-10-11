import pygame
import screeninfo
import sys
import math
import os
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

def main():
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
                       game.level.next()
                elif event.type == pygame.KEYUP:
                    if event.unicode in inputs:
                        game.input_receive(inputs[event.unicode],'remove')
                elif event.type == pygame.MOUSEBUTTONUP:
                    game.mouse_click()
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
    game.menu()
    game.state_manager()

    
    #code end : above this line
    while True:
        if game.state_change:
            game.state_change=0
            game.state_manager()
        display_surface.fill(white)
        game.game_update(display_surface)
        Event_handler()
        fps.show(display_surface)
        
        if game.state[0]=='object_place':
            display_surface.blit(start_word,start_word.get_rect(center=game.start_rect.center))
        elif game.state[0]=='send_map':
            display_surface.blit(wait_word_1,run_word.get_rect(center=game.start_rect.center))
        elif game.state[0]=='receive_map':
            display_surface.blit(wait_word_2,run_word.get_rect(center=game.start_rect.center))
        elif game.state[0]=='ready':
            display_surface.blit(wait_word_3,run_word.get_rect(center=game.start_rect.center))
        elif game.state[0]=='run_phase':
            display_surface.blit(run_word,run_word.get_rect(center=game.start_rect.center))
        pygame.display.update()

        #display_surface.blit(game.console,(0,0))
        #display_surface.blit(grid,(0,0))
        
        #clock.tick(60)

def Quit():
    pygame.quit()
    sys.exit()

#experimental code starts :
from fps import FPS
fps = FPS()
from colors     import *
from fonts      import *
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


start_word=Goldie.render('Send',True,(100,200,10))
run_word=Goldie.render('run',True,(200,10,10))
wait_word_1=Goldie.render('waiting.',True,(200,10,10))
wait_word_2=Goldie.render('waiting..',True,(200,10,10))
wait_word_3=Goldie.render('waiting...',True,(200,10,10))
#experimental code end.

if __name__ == '__main__':
    main()