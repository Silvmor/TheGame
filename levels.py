import pygame
import os

class Level():
    def __init__(self):
        self.SG_0 = pygame.sprite.Group()
        self.SG_1 = pygame.sprite.Group()
        self.background =pygame.Surface((1920,1080))
        self.surface = pygame.Surface((1920,1080))
        self.level_grounds=[]
        num=0
        for img in os.listdir('assets/Level'):
            self.level_grounds.append(pygame.image.load('assets/Level/Level_'+str(num)+'.png'))
            num = num+1

        self.current_level = 1
        self.current_ground = self.level_grounds[self.current_level]
        self.current_rect   = self.current_ground.get_rect()
        self.current_rect.center = (960,550)
        self.surface.blit(self.level_grounds[0],(0,0))
        self.surface.blit(self.current_ground,self.current_rect)
        self.x,self.y,self.w,self.h=0,0,0,0
        self.level_1()

    def next(self):
        self.current_level+=1
        self.current_ground = self.level_grounds[self.current_level]
        self.current_rect   = self.current_ground.get_rect()
        self.current_rect.center = (960,555)
        self.surface.blit(self.level_grounds[0],(0,0))
        self.surface.blit(self.current_ground,self.current_rect)
        #eval call// call = "self.level_"+str(self.current_level)

    def level_1(self):
        self.x,self.y,self.w,self.h=11,6,10,5
        self.occupants=[[0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0]]
    def level_2(self):
        self.x,self.y,self.w,self.h=10,5,12,7
        self.occupants=[[0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0]]
