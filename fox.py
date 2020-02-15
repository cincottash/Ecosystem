class Fox:
	def __init__(self, pos, size):
		#self.color = color
		self.pos = pos
		self.size = size
		
		self.searchRadius = self.size*25
		self.hunger = 100.0
		self.health = 100.0
		self.velocity = 20/size	
		self.timeSinceLastFuck = 0.0