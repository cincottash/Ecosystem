import random
import math

from globals import *
from rabbit import *
from grass import *

global lastGrassPlaceTime

def populateCanvas(desiredRabbitPop, desiredGrassPop):
	currentRabbitPop = 0
	currentGrassPop = 0

	#Populate canvas with rabbits of random size in random loctions, no overlap allowed
	while(currentRabbitPop < desiredRabbitPop):
		placed = 0
		while(placed == 0):
			#Create a random set of cords and a random size
			x = random.randint(-spawnRadius, spawnRadius)+canvasWidth/2
			y = random.randint(-spawnRadius, spawnRadius)+canvasHeight/2
			size = random.randint(minRabbitStartSize, maxRabbitStartSize)

			#check for overlap of rabbits
			canPlace = 1
			for rabbit in rabbitList:
				#distance formula
				distance = math.sqrt((rabbit.pos[0]-x)**2 + (rabbit.pos[1]-y)**2)
				#check for overlap of rabbits
				if(distance <= rabbit.size+size):
					canPlace = 0
					break	

			if(math.sqrt(int(x-canvasWidth/2)**2 + int(y-canvasHeight/2)**2) > spawnRadius):
				canPlace = 0
			
			#If no overlap, we can draw it
			if(canPlace):
				maxHunger = size * 18
				rabbitList.append(Rabbit((x, y), size, maxHunger, random.randint(0, 360)))
				placed = 1
				currentRabbitPop += 1

	#Same thing but for grass, again no overlap of other grass or rabbits
	while(currentGrassPop < desiredGrassPop):
		placed = 0
		while(placed == 0):
			#Create a random set of cords
			x = random.randint(-spawnRadius, spawnRadius)+canvasWidth/2
			y = random.randint(-spawnRadius, spawnRadius)+canvasHeight/2

			#check for overlap of rabbits
			canPlace = 1
			for rabbit in rabbitList:
				#distance formula
				distance = math.sqrt((rabbit.pos[0]-x)**2 + (rabbit.pos[1]-y)**2)
				#8 is the grass size
				if(distance <= rabbit.size*2):
					canPlace = 0
					break

			#if no overlap with rabbits, check the grasses too
			if(canPlace):
				for grass in grassList:
					distance = math.sqrt((grass.pos[0]-x)**2 + (grass.pos[1]-y)**2)
					if(distance <= grass.size*2):
						canPlace = 0
						break		
			
			if(math.sqrt(int(x-canvasWidth/2)**2 + int(y-canvasHeight/2)**2) > spawnRadius):
				canPlace = 0

			#If still no overlap and within the spawnRadius, we can draw it
			if(canPlace):
				grassList.append(Grass(GREEN, (x, y)))
				placed = 1
				currentGrassPop += 1

def updateRabbitStuff():

	rabbitSizes = 0
	for rabbit in rabbitList:
		
		rabbitSizes += rabbit.size
		 
		#Check if rabbit is starving aka the next hunger tick drops hunger leq 0
		if(rabbit.hunger - rabbit.velocity*dt*1500 <= 0):
			#dont let hunger drop below 0 if starving
			rabbit.hunger = 0
			#Since we're starving, check if the next tick of health loss will kill us, we lose health at twice the rate we lose hunger
			if(rabbit.health - rabbit.velocity*dt*3000 <= 0):
				#if it will kill us, remove the rabbit
				rabbitList.remove(rabbit)
				#Dont do other stuff stince we're dead
				continue
			else:
				#otherwise just reduce our health, lose health at twice the rate we lose hunger
				rabbit.health -= rabbit.velocity*dt*3000
		else:
			#if not starving, reduce hunger and increase health by the same amount
			rabbit.hunger -= rabbit.velocity*dt*1500

			rabbit.health += rabbit.velocity*dt*1500

			if(rabbit.health > rabbit.maxHealth):
				rabbit.health = rabbit.maxHealth

		#If not hungry and havent fucked in 20 sec, check for a mate
		if (rabbit.hunger > rabbit.maxHunger/2 and (clock.time() - rabbit.timeOfLastFuck > rabbit.fuckDelay)):
			rabbitSeekMate(rabbit)
		#Search for food if hungry
		elif(rabbit.hunger <= rabbit.maxHunger/2):
			# #Search through grass within searchRadius
			rabbitForage(rabbit)
		#If not hungry just move randomly
		else:
			moveRandomly(rabbit)

	#divide by zero check
	try:
		averageRabbitSize.append(rabbitSizes/len(rabbitList))
	except ZeroDivisionError:
		print("WARNING: All rabbits are dead")
		averageRabbitSize.append(0)

def updateGrassStuff():
	global lastGrassPlaceTime

	#respawn every couple seconds
	if((clock.time() - lastGrassPlaceTime) > grassRespawnDelay):
		placed = 0
		while(placed == 0):
			#Create a random set of cords
			x = random.randint(-spawnRadius, spawnRadius)+canvasWidth/2
			y = random.randint(-spawnRadius, spawnRadius)+canvasHeight/2

			#check for overlap of rabbits
			canPlace = 1
			for rabbit in rabbitList:
				#distance formula
				distance = math.sqrt((rabbit.pos[0]-x)**2 + (rabbit.pos[1]-y)**2)
				if(distance <= rabbit.size*2):
					canPlace = 0
					break

			#if no overlap with rabbits, check the grass too
			if(canPlace):
				for grass in grassList:
					distance = math.sqrt((grass.pos[0]-x)**2 + (grass.pos[1]-y)**2)
					if(distance <= grass.size*2):
						canPlace = 0
						break		
			
			if(math.sqrt(int(x-canvasWidth/2)**2 + int(y-canvasHeight/2)**2) > spawnRadius):
				canPlace = 0

			#If still no overlap, we can draw it
			if(canPlace):
				grassList.append(Grass(GREEN, (x, y)))
				placed = 1
				lastGrassPlaceTime = clock.time()
				#print("Placed grass")

def moveRandomly(animal):

	if((clock.time() - animal.timeOfLastRotation) > animal.timeBeforeRotate):
		animal.theta = random.randint(0, 360)
		animal.timeOfLastRotation = clock.time()
		animal.timeBeforeRotate = random.uniform(3, 6)
	
	dx = animal.velocity*math.cos(animal.theta)
	dy = animal.velocity*math.sin(animal.theta)
	
	boundaryCheck(animal, dx, dy)


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
	dx = rabbit.velocity * math.cos(theta) 
	dy = rabbit.velocity * math.sin(theta)

	rabbit.pos = (rabbit.pos[0] + dx, rabbit.pos[1] + dy)

	#check if a rabbit has reached the nearest piece of food and update stats/delete piece of food
	if(nearestGrassDistance < 5):
		if(rabbit.hunger + grassHealthRegen > rabbit.maxHunger):	
			rabbit.hunger = rabbit.maxHunger
		else:
			rabbit.hunger += grassHealthRegen
		grassList.remove(nearestGrass)
		#print("Reached food")

#offspring has a chance for a mutation to happen when its born, returns new size
def mutate(animalA, animalB):
	mutate = random.randint(1, 100)

	size = (animalA.size+animalB.size)//2

	#if we can mutate, change the size by 25% with a random magnitude
	if(mutate <= mutateProbability):
		magnitude = random.randint(0, 1)

		#if mag is 0, decrease size, if 1 increase it
		if(magnitude == 1):
			#print("mutated larger")
			size = int(size * 1.25)
		else:
			#check if decreasing the size will make the size less than 1 (size has to be at least 1)
			if(int(size * 0.75) < 1):
				#if we can't decrease, just increase instead
				#print("mutated larger")
				size = int(size * 1.25)
			else:
				#print("mutated smaller")
				size = int(size * 0.75)
	return size

def rabbitFuck(rabbit, visibleMates):
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
	dx = rabbit.velocity * math.cos(theta)
	dy = rabbit.velocity * math.sin(theta)
	rabbit.pos = (rabbit.pos[0] + dx, rabbit.pos[1] + dy)

	if(int(nearestMateDistance) < rabbit.size):

		#offspring size is determined within mutate
		size = mutate(rabbit, nearestMate)

		rabbitOffspringHunger = 0.8 * size * 18
		rabbit.timeOfLastFuck = clock.time()
		nearestMate.timeOfLastFuck = clock.time()
		#Make them have sex and spawn a new rabbit
		rabbitList.append(Rabbit(rabbit.pos, size, rabbitOffspringHunger, random.randint(0, 360)))
		#print("Reached mate")

def rabbitForage(rabbit):
	#Search through grass within searchRadius
	visibleGrass = []
	for grass in grassList:
		#Accounts for circle spawnRadius, not just the center coords
		distance = math.sqrt((grass.pos[0] - rabbit.pos[0])**2 + (grass.pos[1] - rabbit.pos[1])**2)-(grass.size + rabbit.size)
		#find closest grass within search area
		if(distance <= rabbit.searchRadius):
			#print("Spotted grass")
			visibleGrass.append(grass)

	if(len(visibleGrass) > 0):
		rabbitEat(rabbit, visibleGrass)
	#If no visible grass, move randomly
	else:
		moveRandomly(rabbit)

def rabbitSeekMate(rabbit):
	#print("searching for mate")
	visibleMates = []
	#Check if any potential mates are within your vision
	for rabbitB in rabbitList:
		#Only go to mate if they're also looking for a mate
		if(rabbitB.hunger > rabbitB.maxHunger/2 and (clock.time() - rabbitB.timeOfLastFuck > rabbit.fuckDelay)):
			#Dont check yourself
			if(rabbitB != rabbit):
				distance = math.sqrt((rabbitB.pos[0] - rabbit.pos[0])**2 + (rabbitB.pos[1] - rabbit.pos[1])**2)-(rabbitB.size + rabbit.size)
				if(distance <= rabbit.searchRadius and distance <= rabbitB.searchRadius):
					#print("See a mate")
					visibleMates.append(rabbitB)

	#If no visible mates, move randomly
	if(len(visibleMates) == 0):
		moveRandomly(rabbit)
	#If there are visible mates, find the closest one and move towards it
	else:
		rabbitFuck(rabbit, visibleMates)


def boundaryCheck(animal, dx, dy):
	
	x = animal.pos[0]
	y = animal.pos[1]

	#If not in range rotate theta by 90
	if(math.sqrt((x-canvasWidth/2+dx)**2 + (y-canvasHeight/2+dy)**2) > spawnRadius):
		animal.theta += rotationAngle
		animal.timeOfLastRotation = clock.time()
		animal.timeBeforeRotate = random.uniform(3, 6)
	else:
		animal.pos = (animal.pos[0] + dx, animal.pos[1] + dy)
