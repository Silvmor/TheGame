import pygame
import screeninfo
from fonts      import *
from colors     import *
from fps import FPS
import sys
import threading


def Server():
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
                    authority(ID,result)
                    chunks.clear()
                continue
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)

    def authority(ID,message):
        RML(message)


    global x,y
    import socket
    port=2300
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((socket.gethostname(),port))
    serverSocket.listen(2)
    RML('Server Logs:\n'+socket.gethostname()+" is now running as "+socket.gethostbyname(socket.gethostname())+" on port "+str(port))
    index=0
    threads=[]
    while index<100:
        connectionSocket, address = serverSocket.accept()
        RML((f"Client_{index} {address} is connected."))
        connections.append(connectionSocket)
        threads.append(threading.Thread(target=connection,args=(connectionSocket,index)))
        threads[index].start()
        index+=1

connections=[]
#initialize
pygame.init()
screen          = screeninfo.get_monitors()[0]
print(screen)
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
                elif event.unicode=='~':
                    exec('log_surface.fill(white);global y;y=50;RML("Server Logs :")')
                elif event.unicode=='`':
                    sender('OK', connections[0])
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

def RML(text,fsize=25,font=NixieOne_small,color=(40,0,40,255)):
    global x,y
    lines = text.splitlines()
    for i, l in enumerate(lines):
        #print(l)
        y +=(fsize*i)
        log_surface.blit(font.render(l,True, color), (x,y))
    y +=fsize



w,h=10,5
server_1_pos=[[ [] for i in range(w)] for i in range(h)]
server_2_pos=[[ [] for i in range(w)] for i in range(h)]
players=[{'ID':'P1','player':[],'opponent':[],'matrix':[[ [] for i in range(w)] for i in range(h)]},
        {'ID':'P2','player':[],'opponent':[],'matrix':[[ [] for i in range(w)] for i in range(h)]}]

fps =FPS()
x,y=10,50
user_text =''
cell_surface= pygame.Surface((1920,1080),pygame.SRCALPHA)
log_surface= pygame.Surface((920,1080))
log_surface.fill(white)
set_matrix(1,1,w,h,server_1_pos)
set_matrix(1,11,w,h,server_2_pos,(255,20,20,100))

surface=pygame.Surface((1920,1080))
surface.fill(white)
surface.blit(cell_surface,(0,0))
surface.blit(Goldie_small.render("Player_1",True,black),(50,10))
surface.blit(Goldie_small.render("Player_2",True,black),(50,510))
server_thread = threading.Thread(target=Server)
server_thread.start()
while True:
    display_surface.fill(white)
    display_surface.blit(surface,(0,0))
    display_surface.blit(log_surface,(1000,0))
    writer(players[0]['matrix'],server_1_pos)
    writer(players[1]['matrix'],server_2_pos)
    
    fps.show(display_surface)
    Event_handler()
    pygame.display.update()     
    #clock.tick(60)