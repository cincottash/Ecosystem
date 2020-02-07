class Rabbit:
	def __init__(self, color, pos, size):
		self.color = color
		self.pos = pos
		self.size = size
		
		self.searchRadius = self.size*10
		self.hunger = 100.0
		self.health = 100.0
		self.velocity = 8/size
		self.timeSinceLastFuck = 0.0