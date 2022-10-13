class Game_World():
	def __init__(self,ID):
		self.data={'ID':ID,'player':[],'opponent':[],'matrix':[[ [] for i in range(w)] for i in range(h)], 'frame' : 0,'HP':0,'took':0,'opponent_HP':0,'opponent_took':0}
