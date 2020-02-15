class Fox:
	def __init__(self, pos, size):
		#self.color = color
		self.pos = pos
		self.size = size
		
		self.searchRadius = self.size*25
		self.hunger = 100.0
		self.health = 50.0
		self.velocity = 30/size	
		self.timeSinceLastFuck = 0.0