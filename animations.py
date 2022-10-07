import pygame
import os
class Animation(pygame.sprite.Sprite):
	def __init__(self,path):
		super().__init__()
		self.play_animation = False
		self.original = []
		num=0
		for img in os.listdir(path):
			self.original.append(pygame.image.load(path+"/"+str(num)+".png"))
			num = num+1
		self.sprites =self.original.copy()
		self.total_sprites =len(self.original)
		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]
		self.rect = self.image.get_rect()
		self.rect.topleft = 0,0

	def update(self,speed):
		if self.play_animation == True:
			self.current_sprite += speed
			if int(self.current_sprite) >= len(self.sprites):
				self.current_sprite = 0
		self.image = self.sprites[int(self.current_sprite)]

	def fade(self,alpha) :
		for sprite in self.sprites :
			sprite.set_alpha(sprite.get_alpha()-alpha)

	def resize(self,width,height) :
		(x,y)=self.rect.center
		self.sprites=self.original.copy()
		for slide in range(len(self.sprites)):
			self.sprites[slide] = pygame.transform.smoothscale(self.sprites[slide],(width,height))
		self.image = self.sprites[int(self.current_sprite)]
		self.rect=self.sprites[0].get_rect()
		self.rect.center=(x,y)

	def zoom(self,fact=1):
		(x,y)=self.rect.center
		width,height=int(self.rect.width*fact),int(self.rect.height*fact)
		self.sprites=self.original.copy()
		for slide in range(len(self.sprites)):
			self.sprites[slide] = pygame.transform.smoothscale(self.sprites[slide],(width,height))
		self.image = self.sprites[int(self.current_sprite)]
		self.rect=self.sprites[0].get_rect()
		self.rect.center=(x,y)

class Still(pygame.sprite.Sprite):
	def __init__(self,path):
		super().__init__()
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect()

	def place(self,pos_x,pos_y,width=None,height=None,fact=None,wrt="TL") :
		if fact :
			width,height=int(self.rect.width*fact),int(self.rect.height*fact)
			self.image=pygame.transform.smoothscale(self.image,(width,height))
		elif width and height :
			self.image=pygame.transform.smoothscale(self.image,(width,height))
		self.rect = self.image.get_rect()
		if wrt=='c':
			self.rect.center = [pos_x,pos_y]
		else:
			self.rect.topleft = [pos_x,pos_y]

	def fade(self,alpha) :
		self.image.set_alpha(alpha)

	def resize(self,width,height) :
		self.image = pygame.transform.smoothscale(self.image,(width,height))
		self.rect = self.image.get_rect()
		