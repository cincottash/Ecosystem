class Rabbit:
	def __init__(self, pos, size):
		#self.color = color
		self.pos = pos
		self.size = size
		
		self.searchRadius = self.size*20
		self.hunger = 100.0
		self.health = 100.0
		self.velocity = 8/(size*1.0)
		self.timeSinceLastFuck = 0.0