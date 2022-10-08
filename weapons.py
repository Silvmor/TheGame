class Weapon():
	def __init__(self):
		pass
	def cryatal_blue(self):
		self.image=Still('assets/weapon/cryatal_blue.png')
		self.image.resize(60,60)
	def cryatal_red(self):
		self.image=Still('assets/weapon/cryatal_red.png')
		self.image.resize(60,60)
	def mine(self):
		self.image=Still('assets/weapon/mine.png')
		self.image.resize(60,60)
	def bomb(self):
		self.image=Still('assets/weapon/bomb.png')
		self.image.resize(50,50)