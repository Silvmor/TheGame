import pygame
import screeninfo
from fonts      import *
from colors     import *
from fps import FPS
import sys
import threading
import ast
import socket


''' initialize '''
pygame.init()
screen          = screeninfo.get_monitors()[0]
clock           = pygame.time.Clock()
display_surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption('Server')

def accept_connections():
    global index,threads
    while index<2:
        connectionSocket, address = serverSocket.accept()
        RML((f"Client_{index} {address} is connected."))
        connections.append(connectionSocket)
        threads.append(threading.Thread(target=connection,args=(connectionSocket,index)))
        threads[index].start()
        index+=1

def connection(sock,ID):
    sock.setblocking(False)
    receiver_thread=threading.Thread(target=receiver,args=(sock,ID))
    receiver_thread.start()
    while True :
        update(sock,ID)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

def sender(msg,sock,ID):
    totalsent = 0
    while totalsent < len(msg):
        sent = sock.send(msg[totalsent:].encode())
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
    RML(msg)

def receiver(sock,ID):
    chunks=[]
    while True:
        try:
            chunk = sock.recv(8).decode("utf-8")
        except:
            if chunks:
                result=''.join(chunks)
                authority(result,sock,ID)
                chunks.clear()
            continue
        if chunk == '':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)

def authority(message,sock,ID):
    global State_ADVANCE
    RML(message)
    split = message.split(',')
    if split.pop(0)=='MS':
        players[ID]['matrix']=ast.literal_eval(message[3:])
        set_player(ID)
        if players[not ID]['player']!=[]:
            set_opponents()
            State_ADVANCE=[1,1]
    elif split.pop(0)=='OK':
        State_ADVANCE[ID]+=1
    elif split.pop(0)=='RR':
        '''here you receive effects in split'''
        pass

def set_player(ID):
    for y,row in enumerate(players[ID]['matrix']):
        for x,cell in enumerate(row):
            if cell!=[]:
                if cell[0] in ['P1','P2']:
                    players[ID]['player']=[x,y]
                    players[not ID]['opponent']=[x,y]

def set_opponents():
    global w,h
    for y,row in enumerate(players[1]['matrix']):
        for x,cell in enumerate(row):
            if cell!=[]:
                if cell[0] in ['P1','P2']:
                    players[0]['matrix'][h-y-1][w-x-1]=['X'+cell[0][1]]
                else:
                    players[0]['matrix'][h-y-1][w-x-1]=cell

    for y,row in enumerate(players[0]['matrix']):
        for x,cell in enumerate(row):
            if cell!=[]:
                if cell[0] in ['P1','P2']:
                    players[1]['matrix'][h-y-1][w-x-1]=['X'+cell[0][1]]
                elif cell[0] in ['X1','X2']:
                    players[1]['matrix'][h-y-1][w-x-1]=['P'+cell[0][1]]

                else:
                    players[1]['matrix'][h-y-1][w-x-1]=cell

    players[0]['matrix'][int(h/2)][0]='CB'
    players[0]['matrix'][int(h/2)-1][0]='Gp'
    players[0]['matrix'][int(h/2)][w-1]='CR'
    players[0]['matrix'][int(h/2)+1][w-1]='Gx'
    players[1]['matrix'][int(h/2)][0]='CB'
    players[1]['matrix'][int(h/2)-1][0]='Gp'
    players[1]['matrix'][int(h/2)][w-1]='CR'
    players[1]['matrix'][int(h/2)+1][w-1]='Gx'

def update(sock,ID):
    if State_ADVANCE==[1,1] or (State_ADVANCE[not ID]==2 and State_ADVANCE[ID]==1):
        '''send matrix'''
        msg=str(players[ID]['matrix'])
        sender(msg,sock,ID)
        State_ADVANCE[ID]+=1
    elif State_ADVANCE==[3,3] or (State_ADVANCE[not ID]==4 and State_ADVANCE[ID]==3):
        '''send KO = begin run_phase'''
        sender('KO',sock,ID)
def forward(message,sock,ID):
    pass
def rollback(message,sock,ID):
    pass



def Event_handler():
    global user_text
    events=pygame.event.get()
    if  events : 
        for event in events :
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_ESCAPE:
                    Quit()
                elif event.key == pygame.K_RETURN :
                    try:
                        exec(user_text)
                        user_text =''
                    except:
                        pass
                elif event.key ==pygame.K_BACKSPACE :
                    user_text=user_text[:-1]
                elif event.unicode=='~':
                    exec('log_surface.fill(white);global y;y=50;RML("Server Logs :")')
                else :
                    user_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONUP:
                pass 
            elif event.type == pygame.QUIT:
                Quit()             
        del events
    pygame.draw.rect(display_surface,black,(50,1010,1820,60),4)
    User_surface = NixieOne.render(user_text,True,red)
    display_surface.blit(User_surface,(70,1020))

def Quit():
    pygame.quit()
    sys.exit()

def set_matrix(x,y,w,h,matrix,color=(0,255,255,100)):
        size=50
        for i in range(h):
            for j in range(w):
                matrix[i][j]=pygame.Rect((x+j)*size,(y+i)*size,size,size)
                pygame.draw.rect(cell_surface,color,((x+j)*size,(y+i)*size,size-3,size-3),border_radius=10)

def writer(matrix,matrix_pos):
    for i,row in enumerate(matrix):
        for j,cell in enumerate(row):
            text=Courier_small.render(str(cell),True,black)
            text_rect=text.get_rect()
            text_rect.center=matrix_pos[i][j].center
            display_surface.blit(text,text_rect)

'''
def make_move(ID,direct):
    player=players[ID]
    opponent=players[not ID]
    player['matrix'][player['player'][0]][player['player'][1]].remove('P')
    player['player'][0]+=move[direct][0]
    player['player'][1]+=move[direct][1]
    player['matrix'][player['player'][0]][player['player'][1]].append('P')

    opponent['matrix'][opponent['opponent'][0]][opponent['opponent'][1]].remove('X')
    opponent['opponent'][0]+=move[direct][0]
    opponent['opponent'][1]-=move[direct][1]
    opponent['matrix'][opponent['opponent'][0]][opponent['opponent'][1]].append('X')
'''

def RML(text,fsize=25,font=NixieOne_small,color=(40,0,40,255)):
    global x,y
    lines = text.splitlines()
    for i, l in enumerate(lines):
        #print(l)
        y +=(fsize*i)
        log_surface.blit(font.render(l,True, color), (x,y))
    y +=fsize

def Load_level(level_number=0):
    global server_1_pos,server_2_pos,w,h
    level_size=[(10,5),(12,7),(16,7),(18,7),(18,9)]
    w,h=level_size[level_number]
    server_1_pos=[[ [] for i in range(w)] for i in range(h)]
    server_2_pos=[[ [] for i in range(w)] for i in range(h)]
    set_matrix(1,1,w,h,server_1_pos)
    set_matrix(1,11,w,h,server_2_pos,(255,20,20,100))

'''connection assignment'''
index=0
port=2300
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(),port))
serverSocket.listen(2)
connections=[]
threads=[]
connection_accept_thread=threading.Thread(target=accept_connections)
connection_accept_thread.start()
'''END'''

'''game variable assignment'''
fps =FPS()
w,h=10,5
x,y=10,50
user_text =''
players=[{'ID':'A','player':[],'opponent':[],'matrix':[[ [] for i in range(w)] for i in range(h)]},
        {'ID':'B','player':[],'opponent':[],'matrix':[[ [] for i in range(w)] for i in range(h)]}]
move   = {'up':[-1,0],'down':[1,0],'left':[0,-1],'right':[0,1]}
State_ADVANCE=[0,0]
'''END'''

''' To display level cell on server screen '''
cell_surface= pygame.Surface((1920,1080),pygame.SRCALPHA)
server_1_pos=[]
server_2_pos=[]
Load_level()
surface=pygame.Surface((1920,1080))
surface.fill(white)
surface.blit(cell_surface,(0,0))
surface.blit(Goldie_small.render("Player_1",True,black),(50,10))
surface.blit(Goldie_small.render("Player_2",True,black),(50,510))
log_surface= pygame.Surface((920,1080))
log_surface.fill(white)
'''END'''
RML('Server Logs:\n'+
    socket.gethostname()+
    " is now running as "+
    socket.gethostbyname(socket.gethostname())+
    " on port "+
    str(port))
while True:
    ''' To run server display,show matrices and logs'''
    display_surface.fill(white)
    display_surface.blit(surface,(0,0))
    display_surface.blit(log_surface,(1000,0))
    writer(players[0]['matrix'],server_1_pos)
    writer(players[1]['matrix'],server_2_pos)
    '''END'''
    
    '''For server to take manual inputs and run local code'''
    fps.show(display_surface)
    Event_handler()
    #update()
    pygame.display.update()     
    #clock.tick(60)