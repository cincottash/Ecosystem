class Fox:
	def __init__(self, pos, size):
		#self.color = color
		self.pos = pos
		self.size = size
		
		self.searchRadius = self.size*40
		self.hunger = 80.0
		self.health = 100.0
		self.velocity = 40/size	
		self.timeSinceLastFuck = 0.0