import pygame
import random
import math

from globals import *
from rabbit import *
from grass import *

pygame.init()

canvas = pygame.display.set_mode((canvasWidth, canvasHeight))

rabbitList = []
grassList = []

def main():

	populateCanvas(2, 25)

	while time < 1000:
		#draw background
		canvas.fill((255,255,255))

		#draw sprites over background
		drawSprites()

		#update sprite attributes
		update()

		#commit changes
		pygame.display.update()


def populateCanvas(startingRabbitPop, startingGrassPop):
	currentRabbitPop = 0
	currentGrassPop = 0

	#Populate canvas with rabbits of random size in random loctions, no overlap of rabbits allowed
	while(currentRabbitPop < startingRabbitPop):
		placed = 0
		while(placed == 0):
			#Create a random set of cords and a random size
			x = random.randint(canvasWidth/4, 3*canvasWidth/4)
			y = random.randint(canvasHeight/4, 3*canvasHeight/4)
			size = random.randint(6, 10)


			#check for overlap of rabbits
			canPlace = 1
			for rabbit in rabbitList:
				#distance formula
				distance = math.sqrt((rabbit.pos[0]-x)**2 + (rabbit.pos[1]-y)**2)
				#check for overlap of rabbits
				if(distance <= rabbit.size+size):
					canPlace = 0
					break	
			#If no overlap, we can draw it
			if(canPlace):
				rabbitList.append(Rabbit((0,0,255), (x, y), size))
				placed = 1
				currentRabbitPop += 1

	#Same thing but for grass, again no overlap of other grass or rabbits
	while(currentGrassPop < startingGrassPop):
		placed = 0
		while(placed == 0):
			#Create a random set of cords
			x = random.randint(canvasWidth/4, 3*canvasWidth/4)
			y = random.randint(canvasHeight/4, 3*canvasHeight/4)

			#check for overlap of rabbits
			canPlace = 1
			for rabbit in rabbitList:
				#distance formula
				distance = math.sqrt((rabbit.pos[0]-x)**2 + (rabbit.pos[1]-y)**2)
				if(distance <= rabbit.size+size):
					canPlace = 0
					break

			#if no overlap with rabbits, check the grass too
			if(canPlace):
				for grass in grassList:
					distance = math.sqrt((grass.pos[0]-x)**2 + (grass.pos[1]-y)**2)
					if(distance <= grass.size+size):
						canPlace = 0
						break		
			
			#If still no overlap, we can draw it
			if(canPlace):
				grassList.append(Grass((0,255,0), (x, y), size))
				placed = 1
				currentGrassPop += 1
				
def drawSprites():
	for rabbit in rabbitList:
		pygame.draw.circle(canvas, rabbit.color, rabbit.pos , rabbit.size)

	for grass in grassList:
		pygame.draw.circle(canvas, grass.color, grass.pos, grass.size)

def update():
	global time

	for rabbit in rabbitList:
		#dont let rabbit health drop below 0
		if(rabbit.hunger - rabbit.size*dt <= 0):
			rabbit.hunger = 0
		else:
			rabbit.hunger -= rabbit.size*dt
		
		#Search for food if hungry(hunger less than half), move randomly if not hungry, or lose health if starving(hunger <= 0)
		if(rabbit.hunger <= 50):
			if(rabbit.hunger <= 0):
				rabbit.health -= rabbit.size*dt

			#Search through grass within searchRadius
			visibleGrass = []
			for grass in grassList:
				#Accounts for circle radius, not just the center coords
				distance = math.sqrt((grass.pos[0] - rabbit.pos[0])**2 + (grass.pos[1] - rabbit.pos[1])**2)-(grass.size + rabbit.size)
				#find closest grass within search area
				if(distance <= rabbit.searchRadius):
					print("Spotted grass")
					visibleGrass.append(grass)

			#Find which of the visible grasses is the closest and move towards it
			if(len(visibleGrass) > 0):
				nearestGrass = visibleGrass[0]
				for grass in visibleGrass: 
					nearestGrassDistance = math.sqrt((nearestGrass.pos[0] - rabbit.pos[0])**2 + (nearestGrass.pos[1] - rabbit.pos[1])**2)
					newDistance = math.sqrt((grass.pos[0] - rabbit.pos[0])**2 + (grass.pos[1] - rabbit.pos[1])**2)
					if(newDistance < nearestGrassDistance):
						nearestGrass = grass
						nearestGrassDistance = newDistance
				
				#Move towards nearest grass
				theta = math.atan2(nearestGrass.pos[1] - rabbit.pos[1], nearestGrass.pos[0] - rabbit.pos[0])
				#had to scale it up a little with * 1.5
				dx = rabbit.velocity * math.cos(theta) * 1.5
				dy = rabbit.velocity * math.sin(theta) * 1.5
				rabbit.pos = (rabbit.pos[0] + int(dx), rabbit.pos[1] + int(dy))

				#check if a rabbit has reached the nearest piece of food and update stats/delete piece of food
				if(int(nearestGrassDistance) == 0):
					rabbit.hunger += 33
					grassList.remove(nearestGrass)
					print("Reached food")
			#If no visible grass, move randomly
			else:

		#print("Rabbit hunger %f rabbit health %f" %(rabbit.hunger, rabbit.health))

		if(rabbit.health <= 0):
			rabbitList.remove(rabbit)

	
	time += dt


if __name__== '__main__':
	main()