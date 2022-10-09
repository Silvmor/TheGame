import pygame
import screeninfo
from fonts      import *
from colors     import *
from fps import FPS

#initialize
pygame.init()
screen          = screeninfo.get_monitors()[0]
clock           = pygame.time.Clock()
display_surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption('Server')

#global variables

inputs          = {'w':'up','a':'left','s':'down','d':'right'}
directions      = {pygame.K_UP:'up',pygame.K_LEFT:'left',pygame.K_DOWN:'down',pygame.K_RIGHT:'right'}
move            = {'up':[-1,0],'down':[1,0],'left':[0,-1],'right':[0,1]}
def Event_handler():
    events=pygame.event.get()
    if  events : 
        for event in events :
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_ESCAPE:
                    Quit()
            elif event.type == pygame.QUIT:
                Quit()             
        del events
def set_matrix(x,y,w,h,matrix):
        size=60
        for i in range(h):
            for j in range(w):
                matrix[i][j]=pygame.Rect((x+j)*size,(y+i)*size,size,size)
                pygame.draw.rect(cell_surface,(0,255,255,100),((x+j)*size,(y+i)*size,size-3,size-3),border_radius=10)

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

def writer(matrix,matrix_pos):
    for i,row in enumerate(matrix):
        for j,cell in enumerate(row):
            text=Courier.render(str(cell),True,black)
            text_rect=text.get_rect()
            text_rect.center=matrix_pos[i][j].center
            display_surface.blit(text,text_rect)

def make_move(number,direct):
    player=players[number]
    opponent=players[not number]
    player['matrix'][player['player'][0]][player['player'][1]].remove('P')
    player['player'][0]+=move[direct][0]
    player['player'][1]+=move[direct][1]
    player['matrix'][player['player'][0]][player['player'][1]].append('P')

    opponent['matrix'][opponent['opponent'][0]][opponent['opponent'][1]].remove('X')
    opponent['opponent'][0]+=move[direct][0]
    opponent['opponent'][1]-=move[direct][1]
    opponent['matrix'][opponent['opponent'][0]][opponent['opponent'][1]].append('X')




w,h=10,5
occupants_1_pos=[[ [] for i in range(w)] for i in range(h)]
occupants_2_pos=[[ [] for i in range(w)] for i in range(h)]

players=[{'ID':'P1','player':[2,0],'opponent':[2,9],'matrix':[[ [] for i in range(w)] for i in range(h)]},
        {'ID':'P2','player':[2,0],'opponent':[2,9],'matrix':[[ [] for i in range(w)] for i in range(h)]}]
players[0]['matrix'][2][0]=['P']
players[0]['matrix'][2][9]=['X']
players[1]['matrix'][2][0]=['P']
players[1]['matrix'][2][9]=['X']

fps =FPS()
cell_surface= pygame.Surface((1920,1080),pygame.SRCALPHA)
set_matrix(1,4,w,h,occupants_1_pos)
set_matrix(17,4,w,h,occupants_2_pos)
surface=pygame.Surface((1920,1080))
surface.fill(white)
surface.blit(cell_surface,(0,0))
#Draw_grid(surface)
make_move(1,'right')
while True:
    display_surface.fill(white)
    display_surface.blit(surface,(0,0))
    writer(players[0]['matrix'],occupants_1_pos)
    writer(players[1]['matrix'],occupants_2_pos)
    fps.show(display_surface)
    Event_handler()
    pygame.display.update()
        
    #clock.tick(60)