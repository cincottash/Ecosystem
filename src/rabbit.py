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
		self.health = self.hunger
		self.velocity = 1/size
		self.maxHunger = self.size * 18
		self.timeOfLastFuck = clock.time()
		self.maxHealth = self.maxHunger
	timeBeforeRotate = random.uniform(3, 6)
	timeOfLastRotation = clock.time()
