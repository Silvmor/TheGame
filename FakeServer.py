import pygame
import screeninfo
from fonts      import *
from colors     import *
from fps import FPS
import sys
import threading


def Server():
    import socket
    import threading
    port=2300
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((socket.gethostname(),port))
    serverSocket.listen(2)
    print(socket.gethostname()," is now running as ->",socket.gethostbyname(socket.gethostname())," on port : ",port)

    def connection(sock,ID):
        running = True
        sock.setblocking(False)
        receiver_thread=threading.Thread(target=receiver,args=(sock,ID))
        receiver_thread.start()
        while running :
            message = input("Send : ")
            if message=='Exit':
                running=False
            else:
                sender(message,sock)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    def sender(msg,sock):
            totalsent = 0
            while totalsent < len(msg):
                sent = sock.send(msg[totalsent:].encode())
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent

    def receiver(sock,ID):
        chunks=[]
        while True:
            try:
                chunk = sock.recv(8).decode("utf-8")
            except:
                if chunks:
                    result=''.join(chunks)
                    authority(str(ID)+' : '+result)
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!")
                    chunks.clear()
                continue
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)

    index=1
    threads=[]
    while 1:
        connectionSocket, address = serverSocket.accept()
        print(f"Client_{index} -> {address} has accepted")
        threads.append(threading.Thread(target=connection,args=(connectionSocket,index)))
        threads[index-1].start()
        index+=1
server_thread = threading.Thread(target=Server)
server_thread.start()


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
                else :
                    user_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONUP:
                controls() 
            elif event.type == pygame.QUIT:
                Quit()             
        del events
    pygame.draw.rect(display_surface,black,(60,960,1320,60),4)
    User_surface = NixieOne.render(user_text,True,red)
    display_surface.blit(User_surface,(80,970))

def Quit():
    pygame.quit()
    sys.exit()

def set_matrix(x,y,w,h,matrix,color=(0,255,255,100)):
        size=60
        for i in range(h):
            for j in range(w):
                matrix[i][j]=pygame.Rect((x+j)*size,(y+i)*size,size,size)
                pygame.draw.rect(cell_surface,color,((x+j)*size,(y+i)*size,size-3,size-3),border_radius=10)

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
            text=Courier_small.render(str(cell),True,black)
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

def RML(text, x, y, fsize=25,font=NixieOne_small,color=(10,200,10,255)) :
    lines = text.splitlines()
    for i, l in enumerate(lines):
        print(l)
        log_surface.blit(font.render(l,True, color), (x, y + fsize*i))

def authority(message):
    RML(message,60,7*60)

w,h=10,5
server_1_pos=[[ [] for i in range(w)] for i in range(h)]
server_2_pos=[[ [] for i in range(w)] for i in range(h)]



players=[{'ID':'P1','player':[2,0],'opponent':[2,9],'matrix':[[ [] for i in range(w)] for i in range(h)]},
        {'ID':'P2','player':[2,0],'opponent':[2,9],'matrix':[[ [] for i in range(w)] for i in range(h)]}]

fps =FPS()
user_text =''
cell_surface= pygame.Surface((1920,1080),pygame.SRCALPHA)
log_surface= pygame.Surface((1920,1080),pygame.SRCALPHA)
set_matrix(1,2,w,h,server_1_pos)
set_matrix(13,2,w,h,server_2_pos)

#client side code
client_1_pos=[[ [] for i in range(w)] for i in range(h)]
client_2_pos=[[ [] for i in range(w)] for i in range(h)]
client=[{'matrix':[[ [] for i in range(w)] for i in range(h)],'player':[2,0]},
        {'matrix':[[ [] for i in range(w)] for i in range(h)],'player':[2,0]}]
client[0]['matrix']=[[[],[],[],[],[],[],[],[],[],[]],
                    [[],[],[],[],['M'],[],[],[],[],[]],
                    [['P'],[],[],['B'],[],[],[],[],[],[]],
                    [[],[],['M'],[],[],[],[],[],[],[]],
                    [[],[],[],[],[],[],[],[],[],[]]]

client[1]['matrix']=[[[],[],[],[],[],[],[],[],[],[]],
                    [[],[],[],[],[],[],[],[],[],[]],
                    [['P'],[],[],['B'],[],[],[],[],[],[]],
                    [[],['M'],[],[],[],[],[],[],[],[]],
                    [['M'],[],[],[],[],[],[],[],[],[]]]

set_matrix(1,9,w,h,client_1_pos,(255,0,0,100))
set_matrix(13,9,w,h,client_2_pos,(255,0,0,100))
client_1_control=[[[],[],[]],[[],[],[]],[[],[],[]]]
client_2_control=[[[],[],[]],[[],[],[]],[[],[],[]]]
set_matrix(24,10,3,3,client_1_control,(255,0,100,100))
set_matrix(28,10,3,3,client_2_control,(255,100,0,100))
control=[['0','up','0'],['left','OK','right'],['+','down','-']]
def mouse_check(matrix):
        pos=pygame.mouse.get_pos()
        for i,row in enumerate(matrix):
            for j,cell in enumerate(row):
                if cell.collidepoint(pos):
                    return [cell,i,j]
        return None
def controls():
    temp = mouse_check(client_1_control)
    if temp:
        if control[temp[1]][temp[2]] in ['+','-']:
            pass
        else:
            client_move(control[temp[1]][temp[2]],0)

    else:
        temp = mouse_check(client_2_control)
        if temp:
            if control[temp[1]][temp[2]] in ['+','-']:
                pass
            else:
                client_move(control[temp[1]][temp[2]],1)

def client_move(direct,index):
    client[index]['matrix'][client[index]['player'][0]][client[index]['player'][1]].remove('P')
    client[index]['player'][0]+=move[direct][0]
    client[index]['player'][1]+=move[direct][1]
    client[index]['matrix'][client[index]['player'][0]][client[index]['player'][1]].append('P')
    #write here what should happen when a client starts to move

surface=pygame.Surface((1920,1080))
surface.fill(white)
surface.blit(cell_surface,(0,0))
surface.blit(Goldie_small.render("server_1",True,black),(1*60,1*60))
surface.blit(Goldie_small.render("server_2",True,black),(13*60,1*60))
surface.blit(Goldie_small.render("client_1",True,black),(1*60,8*60))
surface.blit(Goldie_small.render("client_2",True,black),(13*60,8*60))
#Draw_grid(surface)
while True:
    display_surface.fill(white)
    display_surface.blit(surface,(0,0))
    display_surface.blit(log_surface,(0,0))
    writer(players[0]['matrix'],server_1_pos)
    writer(players[1]['matrix'],server_2_pos)
    writer(client[0]['matrix'],client_1_pos)
    writer(client[1]['matrix'],client_2_pos)
    writer(control,client_1_control)
    writer(control,client_2_control)
    fps.show(display_surface)
    Event_handler()
    pygame.display.update()     
    #clock.tick(60)