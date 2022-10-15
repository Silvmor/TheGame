from animations import Still
from animations import Animation
from explosion import Explosion
class Weapon():
	def __init__(self,ID):
		represent = {'crystal_blue':'CB','crystal_red':'CR','mine':'M','bomb':'B','goal':'Gp','no_goal':'Gx'}
		self.id=represent[ID]
		weapon_call=eval('self.'+ID)
		self.activated=1
		weapon_call()
	def crystal_red(self):
		self.image=Still('assets/weapon/crystal_red.png')
		self.image.resize(70,70)
		self.effect='self.took();self.remove()'
	def mine(self):
		self.image=Still('assets/weapon/mine.png')
		self.image.resize(50,50)
		self.effect='self.take_damage(1);self.remove()'
		self.expl=Explosion()
	def bomb(self):
		self.image=Still('assets/weapon/bomb.png')
		self.image.resize(50,50)
		self.effect='self.take_damage(2);self.remove()'
		self.expl=Explosion()
	def goal(self):
		self.image=Still('assets/weapon/goal.png')
		self.image.resize(70,70)
		self.effect='self.win()'
	def crystal_blue(self):
		self.image=Still('assets/weapon/crystal_blue.png')
		self.image.resize(70,70)
		self.effect='empty'
	def no_goal(self):
		self.effect=''
		self.image=Still('assets/weapon/no_goal.png')
		self.image.resize(70,70)
		self.effect='empty'