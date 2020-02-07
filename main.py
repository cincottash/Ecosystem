import pygame
import random
import math
import time as clock

from globals import *
from rabbit import *
from grass import *

pygame.init()

canvas = pygame.display.set_mode((canvasWidth, canvasHeight))

rabbitList = []
grassList = []

def main():

	populateCanvas(5, 10)

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
			size = random.randint(4, 8)

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
				rabbitList.append(Rabbit((x, y), size))
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
				#8 is the grass size
				if(distance <= rabbit.size+8):
					canPlace = 0
					break

			#if no overlap with rabbits, check the grasses too
			if(canPlace):
				for grass in grassList:
					distance = math.sqrt((grass.pos[0]-x)**2 + (grass.pos[1]-y)**2)
					if(distance <= grass.size*2):
						canPlace = 0
						break		
			
			#If still no overlap, we can draw it
			if(canPlace):
				grassList.append(Grass((0,255,0), (x, y)))
				placed = 1
				currentGrassPop += 1
				
def drawSprites():
	for rabbit in rabbitList:
		
		red = 255 - ((rabbit.hunger/100)*255)
		green = 0
		blue = (rabbit.hunger/100)*255
		
		pygame.draw.circle(canvas, (red, green, blue), (int(rabbit.pos[0]), int(rabbit.pos[1])) , int(rabbit.size))

	for grass in grassList:
		pygame.draw.circle(canvas, grass.color, grass.pos, grass.size)

def update():
	global time
	time = round(time, 3)
	print("Time is: " + str(time))

	#Update all rabbit stuff
	for rabbit in rabbitList:
		rabbit.timeSinceLastFuck += dt
		#dont let rabbit health drop below 0
		if(rabbit.hunger - rabbit.size*dt <= 0):
			rabbit.hunger = 0
			rabbit.health -= rabbit.size*dt
		else:
			rabbit.hunger -= rabbit.size*dt

		#If not hungry and havent fucked in a while check for a mate
		if (rabbit.hunger > 50 and rabbit.timeSinceLastFuck > 5):
			print("searching for mate")
			
			visibleMates = []
			#Check if any potential mates are within your vision
			for rabbitB in rabbitList:
				
				#Only go to mate if they're also looking for a mate
				if(rabbitB.hunger > 50 and rabbitB.timeSinceLastFuck > 5):
					#Dont check yourself
					if(rabbitB != rabbit):
						distance = math.sqrt((rabbitB.pos[0] - rabbit.pos[0])**2 + (rabbitB.pos[1] - rabbit.pos[1])**2)-(rabbitB.size + rabbit.size)
						if(distance <= rabbit.searchRadius):
							print("See a mate")
							visibleMates.append(rabbitB)

			#If no visible mates, move randomly
			if(len(visibleMates) == 0):
				placed = 0

				while(placed == 0):
					#Generate random number to determine the direction we move 
					signX = random.randint(0, 1)
					signY = random.randint(0, 1)

					if(signX == 0):
						signX = -1
					else:
						signX = 1

					if(signY == 0):
						signY = -1
					else:
						signY = 1
					#Check if desired location is within our canvas limits
					if(rabbit.pos[0] + rabbit.size + signX*rabbit.velocity < 3*canvasWidth/4):
						if(rabbit.pos[0] + rabbit.size + signX*rabbit.velocity > canvasWidth/4):
							if(rabbit.pos[1] + rabbit.size + signY*rabbit.velocity > canvasHeight/4):
								if(rabbit.pos[1] + rabbit.size + signY*rabbit.velocity < 3*canvasHeight/4):
									rabbit.pos = (rabbit.pos[0] + signX*rabbit.velocity, rabbit.pos[1] + signY*rabbit.velocity)
									placed = 1
			#If there are visible mates, find the closest one and move towards it
			else:
				nearestMate = visibleMates[0]
				for mate in visibleMates: 
					nearestMateDistance = math.sqrt((nearestMate.pos[0] - rabbit.pos[0])**2 + (nearestMate.pos[1] - rabbit.pos[1])**2)
					newDistance = math.sqrt((mate.pos[0] - rabbit.pos[0])**2 + (mate.pos[1] - rabbit.pos[1])**2)
					if(newDistance < nearestMateDistance):
						nearestMate = mate
						nearestMateDistance = newDistance
				
				#Move towards nearest grass
				theta = math.atan2(nearestMate.pos[1] - rabbit.pos[1], nearestMate.pos[0] - rabbit.pos[0])
				#had to scale it up a little with * 1.5
				dx = rabbit.velocity * math.cos(theta) * 1.5
				dy = rabbit.velocity * math.sin(theta) * 1.5
				rabbit.pos = (rabbit.pos[0] + int(dx), rabbit.pos[1] + int(dy))

				if(int(nearestMateDistance) == 0):
					rabbit.timeSinceLastFuck = 0
					nearestMate.timeSinceLastFuck = 0
					#Make them have sex and spawn a new rabbit by passing averaging the stats of the parental rabbits
					rabbitList.append(Rabbit(rabbit.pos, int((rabbit.size+nearestMate.size)/2)))
					print("Reached mate")

		#Search for food if hungry
		elif(rabbit.hunger <= 50):
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
					rabbit.hunger += 33.0
					grassList.remove(nearestGrass)
					print("Reached food")
			#If no visible grass, move randomly
			else:
				placed = 0

				while(placed == 0):
					#Generate random number to determine the direction we move 
					signX = random.randint(0, 1)
					signY = random.randint(0, 1)

					if(signX == 0):
						#print("signX is " + str(signX))
						signX = -1
					else:
						#print("signX is " + str(signX))
						signX = 1

					if(signY == 0):
						signY = -1
					else:
						signY = 1
					#Check if desired location is within our canvas limits
					if(rabbit.pos[0] + rabbit.size + signX*rabbit.velocity < 3*canvasWidth/4):
						if(rabbit.pos[0] + rabbit.size + signX*rabbit.velocity > canvasWidth/4):
							if(rabbit.pos[1] + rabbit.size + signY*rabbit.velocity > canvasHeight/4):
								if(rabbit.pos[1] + rabbit.size + signY*rabbit.velocity < 3*canvasHeight/4):
									rabbit.pos = (rabbit.pos[0] + signX*rabbit.velocity, rabbit.pos[1] + signY*rabbit.velocity)
									placed = 1
		#If not hungry just move randomly
		else:
			placed = 0

			while(placed == 0):
				#Generate random number to determine the direction we move 
				signX = random.randint(0, 1)
				signY = random.randint(0, 1)

				if(signX == 0):
					signX = -1
				else:
					signX = 1

				if(signY == 0):
					signY = -1
				else:
					signY = 1
				#Check if desired location is within our canvas limits
				if(rabbit.pos[0] + rabbit.size + signX*rabbit.velocity < 3*canvasWidth/4):
					if(rabbit.pos[0] + rabbit.size + signX*rabbit.velocity > canvasWidth/4):
						if(rabbit.pos[1] + rabbit.size + signY*rabbit.velocity > canvasHeight/4):
							if(rabbit.pos[1] + rabbit.size + signY*rabbit.velocity < 3*canvasHeight/4):
								rabbit.pos = (rabbit.pos[0] + signX*rabbit.velocity, rabbit.pos[1] + signY*rabbit.velocity)
								placed = 1
		#print("Rabbit hunger %f rabbit health %f" %(rabbit.hunger, rabbit.health))

		if(rabbit.health <= 0):
			rabbitList.remove(rabbit)

	#Handle grass regrowth
	if(int(time*1000) % 2400*dt  == 0 and int(time) != 0):
		print("time to place")
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
				if(distance <= rabbit.size+8):
					canPlace = 0
					break

			#if no overlap with rabbits, check the grass too
			if(canPlace):
				for grass in grassList:
					distance = math.sqrt((grass.pos[0]-x)**2 + (grass.pos[1]-y)**2)
					if(distance <= grass.size*2):
						canPlace = 0
						break		
			
			#If still no overlap, we can draw it
			if(canPlace):
				grassList.append(Grass((0,255,0), (x, y)))
				placed = 1
				print("Placed grass")
	#dt=.001

	time += dt
	clock.sleep(.050)

if __name__== '__main__':
	main()