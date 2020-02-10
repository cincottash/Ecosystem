class Fox:
	def __init__(self, pos, size):
		#self.color = color
		self.pos = pos
		self.size = size
		
		self.searchRadius = self.size*20
		self.hunger = 67.0
		self.health = 100.0
		self.velocity = 12/(size*1.0)
		self.timeSinceLastFuck = 0.0