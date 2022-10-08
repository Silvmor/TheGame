import pygame
from levels     import Level
from characters import Character
from weapons    import Weapon

class TheGame():
    def __init__(self):
        self.state = 'weapon_place'
        self.characters=[Character('assets/Captain')]
        self.player = self.characters[0]
        self.level = Level()
        self.buffer= []
        self.matrix=[]
        self.inventory=[]
        self.overlay = pygame.Surface((1920,1080),pygame.SRCALPHA)

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
    def load_level(self):
        self.set_matrix()
        self.set_inventory()

    def set_matrix(self):
        size=60
        self.matrix.clear()
        x,y,w,h=self.level.x,self.level.y,self.level.w,self.level.h
        for i in range(h):
            temp=[]
            for j in range(w):
                temp.append(pygame.Rect((x+j)*size,(y+i)*size,size,size))
                pygame.draw.rect(self.overlay,(255,255,255,20),((x+j)*size,(y+i)*size,size-3,size-3),border_radius=20)
            self.matrix.append(temp)

    def set_inventory(self):
        size=90
        self.inventory.clear()
        for i in range(5):
            temp=[]
            for j in range(1):
                temp.append(pygame.Rect(30+(size+30)*j,150+(size+30)*i,size,size))
                pygame.draw.rect(self.overlay,(0,0,0,100),temp[-1],border_radius=20)
            self.inventory.append(temp)
        for i in range(6):
            temp=[]
            for j in range(3):
                temp.append(pygame.Rect(1560+30+(size+15)*j,150+(size+15)*i,size,size))
                pygame.draw.rect(self.overlay,(0,0,0,100),temp[-1],border_radius=20)
            self.inventory.append(temp)

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
