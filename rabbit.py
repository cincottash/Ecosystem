class Rabbit:
	def __init__(self, color, pos, size):
		self.color = color
		self.pos = pos
		self.size = size
		
		self.searchRadius = self.size*4
		self.hunger = 100
		self.thirst = 100
		self.health = 100
		self.velocity = 10/size