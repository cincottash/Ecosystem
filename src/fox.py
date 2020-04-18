class Fox:
	def __init__(self, pos, size, hunger, theta):
		#self.color = color
		self.pos = pos
		self.size = size
		self.theta = theta
		self.searchRadius = self.size*25
		self.hunger = hunger
		self.health = 100.0
		self.velocity = 20/size	
		self.timeSinceLastFuck = 0.0