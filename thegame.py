import pygame
from levels     import Level
from characters import Character
from weapons    import Weapon
from colors     import *
from fonts      import *
from animations import Still
from animations import Animation
from clients import Client
import threading

class TheGame():
    def __init__(self):
        self.state = ['character_choose','free']
        self.state_change=0
        self.player = None
        self.buffer = []

        self.weapons = []
        self.characters=[]

        self.matrix = []
        self.weapon_pos=[]
        self.character_pos=[]

        self.overlay = pygame.Surface((1920,1080),pygame.SRCALPHA)
        self.overlay_fixed = pygame.Surface((1920,1080),pygame.SRCALPHA)
        self.stills=[]
        self.map=['abstract matrix']
        
        #self.console = pygame.Surface((1920,1080),pygame.SRCALPHA)
        #self.con_font=pygame.font.Font("assets/Fonts/NixieOne.otf",30)
        self.effect=''
        self.score=0
        self.current_frame=0
        self.last_update=0

        self.client =Client()

    def state_manager(self):
        if self.state[0]=='run_phase':
            self.start_frame()
        elif self.state[0]=='send_map':
            self.client.sender('MS,'+str(self.map))
        elif self.state[0]=='receive_map':
            self.set_opponent()
        elif self.state[0]=='ready':
            self.client.sender('OK')
        elif self.state[0]=='object_place':
            self.set_matrix()
            self.set_inventory()
            self.character_assign()
            self.weapon_assign()
            self.goal_set()
            self.start()
            self.legend()
            self.level.surface.blit(self.overlay_fixed,(0,0))
        elif self.state[0]=='character_choose':
                self.character_choose()
                self.state=['object_place','free']
                self.level = Level()
                self.state_change=1
        elif self.state[0]=='win':
            self.state=['object_place','free']
            if self.level.next()=='credits':
                self.state=['credits']
                print('Thank You For Playing.')
            self.stills.clear()
            self.player=None
            self.state_change=1

    def game_update(self,surface):
        
        if self.state[0] in ['object_place','run_phase']:
            surface.blit(self.level.surface,(0,0))
            if self.state[0]=='object_place':
                cell=None
                temp=[self.mouse_check(self.matrix) or self.mouse_check(self.character_pos) or self.mouse_check(self.weapon_pos)]
                if self.state[1]!='free':
                    cell=eval(f"self.{self.state[1]}[{self.state[2][0]}][{self.state[2][1]}]")
                    self.draw_select(surface,(200,0,0,50),cell)
                if temp[0]:
                    if temp[0][0]!=cell:
                        self.draw_select(surface,(0,200,200,50),temp[0][0])
                    else:
                        self.draw_select(surface,(100,0,0,255),cell,0)

            elif self.state[0]=='run_phase':
                self.current_frame+=1
                if self.player.state=='walk':
                    if self.player.wait>0:
                        self.player.walk()
                        self.player.wait-=1
                        if self.player.wait==0:
                            self.use_effect()
                            self.set_wait()

            surface.blit(Courier.render('Wins    : '+str(self.score),True,black),(30,960))
            for image in self.stills:
                image.draw(surface)
            if self.player:
                self.player.SG.draw(surface)
                surface.blit(Courier.render('Hp      : '+str(self.player.HP),True,black),(30,990))
                surface.blit(Courier.render('Reveals : '+str(self.player.reveals),True,black),(30,1020))
        elif self.state[0]=='send_map':
            if self.client.authority_advance:
                self.state[0]='receive_map'
        elif self.state[0]=='ready':
            if self.client.authority_advance:
                self.state[0]=='run_phase'

    #initial phase
    def menu(self):
        self.client =Client()
        IP=0
        client_thread=threading.Thread(target=self.client.connect(),args=(IP,))
        client_thread.start()

    def character_choose(self):
        #after finished
        self.characters=[Character('Captain'),Character('Spy'),Character('Spy'),Character('Captain'),Character('Captain'),Character('Spy')]
    
    ##phase 'object_place'
    #1.level initialize
    def set_matrix(self):
        size=60
        self.matrix.clear()
        x,y,w,h=self.level.x,self.level.y,self.level.w,self.level.h
        for i in range(h):
            temp=[]
            for j in range(w):
                temp.append(pygame.Rect((x+j)*size,(y+i)*size,size,size))
                pygame.draw.rect(self.overlay_fixed,(255,255,255,20),((x+j)*size,(y+i)*size,size-3,size-3),border_radius=20)
            self.matrix.append(temp)
        self.map=[[ [] for i in range(w)] for i in range(h)]

    def set_inventory(self):
        self.character_pos.clear()
        self.weapon_pos.clear()
        for i in range(6):
            temp=[]
            for j in range(1):
                temp.append(pygame.Rect(60+(90+30)*j,150+(90+30)*i,90,90))
                pygame.draw.rect(self.overlay_fixed,(50,50,50,100),temp[-1],border_radius=20)
                pygame.draw.rect(self.overlay_fixed,(0,0,0,100),temp[-1],width=5,border_radius=20)
            self.character_pos.append(temp)
        for i in range(int(len(self.level.allowed_weapon)/3)):
            temp=[]
            for j in range(3):
                temp.append(pygame.Rect(1560+30+(90+15)*j,150+(90+15)*i,90,90))
                pygame.draw.rect(self.overlay_fixed,(50,50,50,100),temp[-1],border_radius=20)
                pygame.draw.rect(self.overlay_fixed,(0,0,0,100),temp[-1],width=5,border_radius=20)
            self.weapon_pos.append(temp)

    #2.level screen setup
    def character_assign(self):
        for index,character in enumerate(self.characters):
            temp=Still('assets/character/'+character.name+'.png')
            temp.zoom(1.2)
            cell=self.character_pos[index][0]
            temp.place(cell.center[0],cell.center[1]-10,wrt='c')
            temp.draw(self.overlay_fixed)

    def weapon_assign(self):
        #to be chnged to support numbers
        for index,name in enumerate(self.level.allowed_weapon):
            temp=Still('assets/Weapon/'+name+'.png')
            temp.resize(70,70)
            cell=self.weapon_pos[int(index/3)][index%3]
            temp.place(cell.center[0],cell.center[1],wrt='c')
            temp.draw(self.overlay_fixed)
            self.weapons.append([name,self.level.counts[index]])

    def goal_set(self):
        temp=Weapon('crystal_blue')
        temp.image.rect.center=self.matrix[int(self.level.h/2)][0].center
        self.stills.append(temp.image)

        self.level.occupants[0][int(self.level.h/2)]=[['block',temp]]

        temp=Weapon('goal')
        temp.image.rect.center=self.matrix[int(self.level.h/2)-1][0].center
        self.stills.append(temp.image)
        self.level.occupants[0][int(self.level.h/2)-1]=[['weapon',temp]]

        temp=Weapon('crystal_red')
        temp.image.rect.center=self.matrix[int(self.level.h/2)][self.level.w-1].center
        self.stills.append(temp.image)
        self.level.occupants[self.level.w-1][int(self.level.h/2)]=[['weapon',temp]]

        temp=Weapon('no_goal')
        temp.image.rect.center=self.matrix[int(self.level.h/2)+1][self.level.w-1].center
        self.stills.append(temp.image)
        self.level.occupants[self.level.w-1][int(self.level.h/2)+1]=[['weapon',temp]]

    #3.receive input
    def mouse_click(self):
        #code in character,initial phase
        if self.state[0]=='object_place':
            if self.start_rect.collidepoint(pygame.mouse.get_pos()):
                if self.player:
                    self.state=["send_map",'free']
                    self.state_change=1
            else:
                temp=self.mouse_check(self.matrix)
                if temp:
                    if temp[1]<self.level.w and temp[2]<self.level.h:
                        if self.state[1] in ['free','matrix']:
                            self.state=['object_place','matrix',[temp[1],temp[2]]]
                        else:
                            if self.state[1]=='weapon_pos':
                                self.weapon_place(self.state[2][0],self.state[2][1],temp[1],temp[2])
                            elif self.state[1]=='character_pos':
                                self.character_place(self.state[2][0],self.state[2][1],temp[1],temp[2])
                            self.state=['object_place','free']
                        
                else:
                    temp=self.mouse_check(self.weapon_pos)
                    if temp:
                        #check for validity
                        if self.state[1] in ['free','weapon_pos','character_pos']:
                            self.state=self.state=['object_place','weapon_pos',[temp[1],temp[2]]]
                        elif self.state[1]=='matrix':
                            self.weapon_place(temp[1],temp[2],self.state[2][0],self.state[2][1])
                            self.state=['object_place','free']

                    else:
                        temp=self.mouse_check(self.character_pos)
                        if temp:
                            if self.state[1] in ['free','weapon_pos','character_pos']:
                                self.state=self.state=['object_place','character_pos',[temp[1],temp[2]]]
                            elif self.state[1]=='matrix':
                                self.character_place(temp[1],temp[2],self.state[2][0],self.state[2][1])
                                self.state=['object_place','free']
                        else:
                            self.state=['object_place','free']
                            
    def mouse_check(self,matrix):
        pos=pygame.mouse.get_pos()
        for i,row in enumerate(matrix):
            for j,cell in enumerate(row):
                if cell.collidepoint(pos):
                    return [cell,i,j]
        return None

    def draw_select(self,screen,color,rect,fill=1):
            Surface=pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
            if fill:
                pygame.draw.rect(Surface,(255,255,255,100),(0,0,rect.width,rect.height),border_radius=20)
            pygame.draw.rect(Surface,color,(0,0,rect.width,rect.height),width=5,border_radius=20)
            screen.blit(Surface,rect.topleft)
            del Surface

    #4.placement of objects
    def character_place(self,from_x,from_y,to_x,to_y):
        if self.level.occupants[to_y][to_x]==[]:
            if self.player:
                self.level.occupants[self.player.position[0]][self.player.position[1]]=[]
                self.map[self.player.position[0]][self.player.position[1]]=[]
            self.player=self.characters[from_x]
            self.player.position=[to_y,to_x]
            self.level.occupants[to_y][to_x]=[['block','P1']]
            self.map[to_x][to_y]=['P']
            self.player.animation.rect.center = ((self.level.x+to_y)*60+30,(self.level.y+to_x)*60-10)
    
    def weapon_place(self,from_x,from_y,to_x,to_y):
        if self.level.occupants[to_y][to_x]==[]:
            temp=Weapon(self.weapons[from_x*3+from_y][0])
            temp.image.rect.center=self.matrix[to_x][to_y].center
            self.level.occupants[to_y][to_x]=[['weapon',temp]]
            self.map[to_x][to_y]=[temp.id]
            self.stills.append(temp.image)


    #phase 'run phase'
    def input_receive(self,direction,state):
        #code in run phase
        if self.state[0]=='run_phase':
            if direction!='yes' and direction!='no':
                if state=='remove':
                    if direction in self.buffer:
                        self.buffer.remove(direction)
                elif state=='walk':
                    self.buffer.append(direction)
                    if self.player.wait==0:
                        self.set_wait()
                        self.player.direction=direction
                        self.player.idle(change=True)
            elif direction=='yes':
                pass

    def set_wait(self):
        if self.buffer:
            while self.buffer:
                entry=self.buffer[-1]
                if self.validate_move(entry):
                    self.client.sender('RR,'+str(self.current_frame)+','+self.effect)
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
        if not self.buffer:
            self.player.wait=0
            self.player.state='idle'

    def validate_move(self,entry):
        move = {"up":[0,-1],"down":[0,1],"left":[-1,0],"right":[1,0]}
        new_x=self.player.position[0]+move[entry][0]
        new_y=self.player.position[1]+move[entry][1]
        if new_x in range(self.level.w):
            if new_y in range(self.level.h):
                occupant = self.level.occupants[new_x][new_y]
                if occupant==[]:
                    self.effect=f"self.move({new_x},{new_y})"
                    return 1
                elif occupant[0][0]=='weapon':
                    if occupant[0][1].activated:
                        self.effect=f"self.move({new_x},{new_y}),{occupant[0][1].effect}"
                    return 1
                else:
                   print("In front : ",occupant)

    def move(self,x,y):
        self.level.occupants[self.player.position[0]][self.player.position[1]].remove(['block','P1'])
        self.level.occupants[x][y].append(['block','P1'])
        self.player.position=[x,y]
    def undo_move(self,x,y):
        self.level.occupants[self.player.position[0]][self.player.position[1]].remove(['block','P1'])
        self.level.occupants[x][y].append(['block','P1'])
        self.player.position=[x,y]
    def take_damage(self,amount):
        self.player.HP-=amount
        #could be in negative
    def undo_take_damage(self,amount):
        self.player.HP+=amount
    def remove(self):
        temp=self.level.occupants[self.player.position[0]][self.player.position[1]][0]
        temp[1].activated=0
        self.stills.remove(temp[1].image)
    def undo_remove(self):
        temp=self.level.occupants[self.player.position[0]][self.player.position[1]][0]
        temp.activated=1
        self.stills.append(temp[1].image)
    def took(self):
        self.state[1]='took'
    def undo_took(self):
        self.state[1]='free'
    def win(self):
        if self.state[1]=='took':
            #here first resolve all conflicts
            self.score+=1
            self.state=['win']
            self.state_change=1

    def use_effect(self):
        self.client.sender('RR,'+self.effect)
        eval(self.effect)
        self.effect=''

    def rollback(self,effect):
        eval(effect)

    def legend(self):
        character_word=Goldie.render('Character',True,black)
        weapon_word=Goldie.render('Weapon',True,black)
        self.overlay_fixed.blit(character_word,(60,60))
        self.overlay_fixed.blit(weapon_word,(1590,60))
    def start(self):
        self.start_rect=pygame.Rect(840,960,240,90)
        pygame.draw.rect(self.overlay_fixed,(50,50,50,100),self.start_rect,border_radius=20)
        pygame.draw.rect(self.overlay_fixed,(0,0,0,100),self.start_rect,width=5,border_radius=20)

    def set_opponent(self):
        temp_matrix=self.client.authority_messages.pop(0)
        self.state[0]='ready'
    def start_frame(self):
        self.client.authority_messages.pop(0)

