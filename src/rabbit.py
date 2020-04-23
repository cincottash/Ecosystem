from globals import *
import random
class Rabbit:
	def __init__(self, pos, size, hunger, theta):
		#self.color = color
		self.pos = pos
		self.size = size
		self.theta = theta
		self.searchRadius = self.size*30
		self.hunger = hunger
		self.health = 100.0
		self.velocity = 12/size
		self.timeOfLastFuck = clock.time()
	timeBeforeRotate = random.uniform(3, 6)
	timeOfLastRotation = clock.time()