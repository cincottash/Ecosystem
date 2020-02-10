import random
import math
import time as clock

from globals import *
from rabbit import *
from grass import *

def populateCanvas(startingRabbitPop, startingGrassPop):
	currentRabbitPop = 0
	currentGrassPop = 0

	#Populate canvas with rabbits of random size in random loctions, no overlap of rabbits allowed
	while(currentRabbitPop < startingRabbitPop):
		placed = 0
		while(placed == 0):
			#Create a random set of cords and a random size
			x = random.randint(int(canvasWidth/6), int(5*canvasWidth/6))
			y = random.randint(int(canvasHeight/6), int(5*canvasHeight/6))
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
				rabbitList.append(Rabbit((x, y), size))
				placed = 1
				currentRabbitPop += 1

	#Same thing but for grass, again no overlap of other grass or rabbits
	while(currentGrassPop < startingGrassPop):
		placed = 0
		while(placed == 0):
			#Create a random set of cords
			x = random.randint(int(canvasWidth/6), int(5*canvasWidth/6))
			y = random.randint(int(canvasHeight/6), int(5*canvasHeight/6))

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
				grassList.append(Grass(GREEN, (x, y)))
				placed = 1
				currentGrassPop += 1

def updateRabbitStuff():
	rabbitSizes = 0
	for rabbit in rabbitList:
		rabbitSizes += rabbit.size
		rabbit.timeSinceLastFuck += dt
		
		#Check if rabbit is starving aka the next hunger tick drops hunger leq 0
		if(rabbit.hunger - rabbit.size*dt*300 <= 0):
			#dont let hunger drop below 0 if starving
			rabbit.hunger = 0
			#Since we're starving, check if the next tick of health loss will kill us
			if(rabbit.health - rabbit.size*dt*300 <= 0):
				#if it will kill us, remove the rabbit
				rabbitList.remove(rabbit)
				#Dont do other stuff stince we're dead
				continue
			else:
				#otherwise just reduce our health
				rabbit.health -= rabbit.size*dt*300
		else:
			#if not starving, reduce health
			rabbit.hunger -= rabbit.size*dt*300

		#If not hungry and havent fucked in a while check for a mate
		if (rabbit.hunger > 50 and rabbit.timeSinceLastFuck > 0.01):
			#print("searching for mate")
			visibleMates = []
			#Check if any potential mates are within your vision
			for rabbitB in rabbitList:
				#Only go to mate if they're also looking for a mate
				if(rabbitB.hunger > 50 and rabbitB.timeSinceLastFuck > 0.01):
					#Dont check yourself
					if(rabbitB != rabbit):
						distance = math.sqrt((rabbitB.pos[0] - rabbit.pos[0])**2 + (rabbitB.pos[1] - rabbit.pos[1])**2)-(rabbitB.size + rabbit.size)
						if(distance <= rabbit.searchRadius):
							#print("See a mate")
							visibleMates.append(rabbitB)

			#If no visible mates, move randomly
			if(len(visibleMates) == 0):

				moveRandomly(rabbit)
			
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
					rabbit.timeSinceLastFuck = 0.0
					nearestMate.timeSinceLastFuck = 0.0
					#Make them have sex and spawn a new rabbit by averaging the stats of the parental rabbits
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
					#print("Spotted grass")
					visibleGrass.append(grass)

			#Find which of the visible grasses is the closest and move towards it
			if(len(visibleGrass) > 0):
				rabbitEat(rabbit, visibleGrass)
			#If no visible grass, move randomly
			else:
				moveRandomly(rabbit)
		#If not hungry just move randomly
		else:
			moveRandomly(rabbit)
		#print("Rabbit hunger %f rabbit health %f" %(rabbit.hunger, rabbit.health))

	#divide by zero check
	try:
		averageRabbitSize.append(float(rabbitSizes)/len(rabbitList))
	except ZeroDivisionError:
		print("WARNING: All rabbits are dead")

def updateGrassStuff(time1):
	#Handle grass regrowth
	currentTime = time1
	#print(int(currentTime*10000.0 % 30))
	if(int(currentTime*10000.0 % 30) == 0 and int(currentTime*10000.0) > 0):
		#print("placing grass at %s" % currentTime)
		placed = 0
		while(placed == 0):
			#Create a random set of cords
			x = random.randint(int(canvasWidth/6), int(5*canvasWidth/6))
			y = random.randint(int(canvasHeight/6), int(5*canvasHeight/6))

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
				grassList.append(Grass(GREEN, (x, y)))
				placed = 1
				print("Placed grass")

def moveRandomly(animal):
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
	animal.pos = (animal.pos[0] + signX*animal.velocity, animal.pos[1] + signY*animal.velocity)

def rabbitEat(rabbit, visibleGrass):
	nearestGrass = visibleGrass[0]
	for grass in visibleGrass: 
		#just start with the closest grass being the first visible one
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
	if(nearestGrassDistance < 5):
		if(rabbit.hunger + 33.0 > 100.0):	
			rabbit.hunger = 100.0
		else:
			rabbit.hunger += 33.0
		grassList.remove(nearestGrass)
		print("Reached food")