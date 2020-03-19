class Rabbit:
	def __init__(self, pos, size, hunger):
		#self.color = color
		self.pos = pos
		self.size = size
		
		self.searchRadius = self.size*30
		self.hunger = hunger
		self.health = 100.0
		self.velocity = 12/size
		self.timeSinceLastFuck = 0.0