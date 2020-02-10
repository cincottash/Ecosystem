class Fox:
	def __init__(self, pos, size):
		#self.color = color
		self.pos = pos
		self.size = size
		
		self.searchRadius = self.size*30
		self.hunger = 67.0
		self.health = 0.0
		self.velocity = 5	
		self.timeSinceLastFuck = 0.0