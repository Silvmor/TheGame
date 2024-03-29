import pygame
import os


class Level:
    '''Class which controls levels of the game'''
    def __init__(self):
        self.background = pygame.Surface((1920, 1080))
        self.surface = pygame.Surface((1920, 1080))
        self.level_grounds = []
        num = 0
        for img in os.listdir("assets/Level"):
            self.level_grounds.append(
                pygame.image.load(
                    "assets/Level/Level_" + str(num) + ".png"
                ).convert_alpha()
            )
            num = num + 1

        self.current_level = 0
        self.next()

    def next(self):
        '''Loads the next level'''
        self.current_level += 1
        self.current_ground = self.level_grounds[self.current_level]
        self.current_rect = self.current_ground.get_rect()
        self.current_rect.center = (960, 550)
        self.surface.blit(self.level_grounds[0], (0, 0))
        self.surface.blit(self.current_ground, self.current_rect)
        level_call = eval("self.level_" + str(self.current_level))
        return level_call()

    def level_1(self):
        '''Level 1'''
        self.x, self.y, self.w, self.h = 11, 6, 10, 5
        self.occupants = [[[] for i in range(self.h)] for i in range(self.w)]
        self.allowed_weapon = ["mine", "mine", "mine"]
        self.weapon_counts = [1, 1, 1]

    def level_2(self):
        '''Level 2'''
        self.x, self.y, self.w, self.h = 10, 5, 12, 7
        self.occupants = [[[] for i in range(self.h)] for i in range(self.w)]
        self.allowed_weapon = ["mine", "bomb", "mine"]
        self.weapon_counts = [1, 1, 1]

    def level_3(self):
        '''Level 3'''
        self.x, self.y, self.w, self.h = 8, 5, 16, 7
        self.occupants = [[[] for i in range(self.h)] for i in range(self.w)]
        self.allowed_weapon = ["mine", "bomb", "mine", "bomb", "mine", "bomb"]
        self.weapon_counts = [1, 1, 1, 1, 1, 1]

    def level_4(self):
        '''Level 4'''
        self.x, self.y, self.w, self.h = 7, 5, 18, 7
        self.occupants = [[[] for i in range(self.h)] for i in range(self.w)]
        self.allowed_weapon = ["mine", "bomb", "mine", "bomb", "bomb", "bomb"]
        self.weapon_counts = [1, 1, 1, 1, 1, 1]

    def level_5(self):
        '''Level 5'''
        self.x, self.y, self.w, self.h = 7, 4, 18, 9
        self.occupants = [[[] for i in range(self.h)] for i in range(self.w)]
        self.allowed_weapon = [
            "bomb",
            "bomb",
            "bomb",
            "bomb",
            "bomb",
            "bomb",
            "mine",
            "bomb",
            "mine",
        ]
        self.weapon_counts = [1, 1, 1, 1, 1, 1, 1, 1, 1]

    def level_6(self):
        '''Level 6'''
        return "credits"
