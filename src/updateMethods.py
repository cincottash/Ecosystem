import random
import math

from globals import *
from rabbit import *
from grass import *
from fox import *

global lastGrassPlaceTime

def populateCanvas(desiredRabbitPop, desiredGrassPop, desiredFoxPop):
	currentRabbitPop = 0
	currentGrassPop = 0
	currentFoxPop = 0

	#Populate canvas with rabbits of random size in random loctions, no overlap of rabbits allowed
	while(currentRabbitPop < desiredRabbitPop):
		placed = 0
		while(placed == 0):
			#Create a random set of cords and a random size
			x = random.randint(-spawnRadius, spawnRadius)+canvasWidth/2
			y = random.randint(-spawnRadius, spawnRadius)+canvasHeight/2
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

			if(math.sqrt(int(x-canvasWidth/2)**2 + int(y-canvasHeight/2)**2) > spawnRadius):
				canPlace = 0
			
			#If no overlap, we can draw it
			if(canPlace):
				rabbitList.append(Rabbit((x, y), size, 100, random.randint(0, 360)))
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
	#Same thing but for foxes, again no overlap of other grass, rabbits or foxes
	
	while(currentFoxPop < desiredFoxPop):
		placed = 0
		while(placed == 0):
			#Create a random set of cords
			x = random.randint(-spawnRadius, spawnRadius)+canvasWidth/2
			y = random.randint(-spawnRadius, spawnRadius)+canvasHeight/2
			size = random.randint(10, 14)

			#check for overlap of rabbits
			canPlace = 1
			for rabbit in rabbitList:
				#distance formula
				distance = math.sqrt((rabbit.pos[0]-x)**2 + (rabbit.pos[1]-y)**2)
				#*2 is a spcaer
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
			if(canPlace):
				for fox in foxList:
					distance = math.sqrt((fox.pos[0]-x)**2 + (fox.pos[1]-y)**2)
					if(distance <= fox.size*2):
						canPlace = 0
						break

			if(math.sqrt(int(x-canvasWidth/2)**2 + int(y-canvasHeight/2)**2) > spawnRadius):
				canPlace = 0

			#If still no overlap, we can draw it
			if(canPlace):
				#Just give it a size of 10 for now
				foxList.append(Fox((x, y), size, 100, random.randint(0, 360)))
				placed = 1
				currentFoxPop += 1


def updateRabbitStuff():

	rabbitSizes = 0
	for rabbit in rabbitList:
		rabbitSizes += rabbit.size
		 
		#Check if rabbit is starving aka the next hunger tick drops hunger leq 0
		if(rabbit.hunger - rabbit.size*dt*10 <= 0):
			#dont let hunger drop below 0 if starving
			rabbit.hunger = 0
			#Since we're starving, check if the next tick of health loss will kill us
			if(rabbit.health - rabbit.size*dt*10 <= 0):
				#if it will kill us, remove the rabbit
				rabbitList.remove(rabbit)
				#Dont do other stuff stince we're dead
				continue
			else:
				#otherwise just reduce our health
				rabbit.health -= rabbit.size*dt*10
		else:
			#if not starving, reduce hunger
			rabbit.hunger -= rabbit.size*dt*10

		#Prioritize running from foxes over eating and fucking
		if(checkForPredators(rabbit) == False):
			#If not hungry and havent fucked in 20 sec, check for a mate
			if (rabbit.hunger > 50 and (clock.time() - rabbit.timeOfLastFuck > 20)):
				rabbitSeekMate(rabbit)
			#Search for food if hungry
			elif(rabbit.hunger <= 50):
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

def updateGrassStuff():
	global lastGrassPlaceTime

	#respawn every 3.5 seconds
	if((clock.time() - lastGrassPlaceTime) > 5.0):
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
	


	##respawn every 15 seconds
	#if((clock.time() - lastGrassPlaceTime) > 3):


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
		if(rabbit.hunger + 50.0 > 100.0):	
			rabbit.hunger = 100.0
		else:
			rabbit.hunger += 50.0
		grassList.remove(nearestGrass)
		#print("Reached food")

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

	if(int(nearestMateDistance) < 10):
		rabbit.timeOfLastFuck = clock.time()
		nearestMate.timeOfLastFuck = clock.time()
		#Make them have sex and spawn a new rabbit by averaging the stats of the parental rabbits
		rabbitList.append(Rabbit(rabbit.pos, int((rabbit.size+nearestMate.size)/2), 80, random.randint(0, 360)))
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

def checkForPredators(rabbit):
	visiblePredators = []
	for fox in foxList:
		distance = math.sqrt((fox.pos[0] - rabbit.pos[0])**2 + (fox.pos[1] - rabbit.pos[1])**2)
		#find closest grass within search area
		if(distance <= rabbit.searchRadius):
			#print("Spotted Fox!!!")
			visiblePredators.append(fox)
	if(len(visiblePredators) > 0):
		#Find the clostest predator to yourself
		nearestPredator = visiblePredators[0]
		for predator in visiblePredators: 
			nearestPredatorDistance = math.sqrt((nearestPredator.pos[0] - rabbit.pos[0])**2 + (nearestPredator.pos[1] - rabbit.pos[1])**2)
			newDistance = math.sqrt((predator.pos[0] - rabbit.pos[0])**2 + (predator.pos[1] - rabbit.pos[1])**2)
			if(newDistance < nearestPredatorDistance):
				nearestPredator = predator
				nearestPredatorDistance = newDistance

		#Run away from it
		theta = math.atan2(nearestPredator.pos[1] - rabbit.pos[1], nearestPredator.pos[0] - rabbit.pos[0])
		#-1 to go the opposite direction
		dx = rabbit.velocity * math.cos(theta) * -1
		dy = rabbit.velocity * math.sin(theta) * -1

		#check if we're over the screen boundary
		boundaryCheck(rabbit, dx, dy)
		
		return True
	else:
		return False

def rabbitSeekMate(rabbit):
	#print("searching for mate")
	visibleMates = []
	#Check if any potential mates are within your vision
	for rabbitB in rabbitList:
		#Only go to mate if they're also looking for a mate
		if(rabbitB.hunger > 50 and (clock.time() - rabbitB.timeOfLastFuck > 20)):
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
		rabbitFuck(rabbit, visibleMates)


def updateFoxStuff():
	for fox in foxList:
		
		fox.timeOfLastFuck += dt
		
		#Check if rabbit is starving aka the next hunger tick drops hunger leq 0
		if(fox.hunger - fox.size*dt*300 <= 0):
			#dont let hunger drop below 0 if starving
			fox.hunger = 0
			#Since we're starving, check if the next tick of health loss will kill us
			if(fox.health - fox.size*dt*300 <= 0):
				#if it will kill us, remove the rabbit
				foxList.remove(fox)
				#Dont do other stuff stince we're dead
				continue
			else:
				#otherwise just reduce our health
				fox.health -= fox.size*dt*300
		else:
			#if not starving, reduce health
			fox.hunger -= fox.size*dt*300

	#If not hungry and havent fucked in a while check for a mate
		if (fox.hunger > 50 and fox.timeOfLastFuck > 0.01):
			#rabbitSeekMate(rabbit)
			#print("Looking for mate")
			
			foxSeekMate(fox)
		#Search for food if hungry
		elif(fox.hunger <= 50):
			#Search through grass within searchRadius
			#rabbitForage(rabbit)
			foxForage(fox)
		
		#If not hungry just move randomly
		else:
			moveRandomly(fox)

	#divide by zero check
	try:
	 	len(foxList)
	except ZeroDivisionError:
	 	print("WARNING: All foxes are dead")

def foxForage(fox):
	#Search through grass within searchRadius
	visibleRabbits = []
	for rabbit in rabbitList:
		#Accounts for circle spawnRadius, not just the center coords
		distance = math.sqrt((rabbit.pos[0] - fox.pos[0])**2 + (rabbit.pos[1] - fox.pos[1])**2)
		#find closest grass within search area
		if(distance <= fox.searchRadius):
			#print("Spotted grass")
			visibleRabbits.append(rabbit)

	if(len(visibleRabbits) > 0):
		#rabbitEat(rabbit, visibleGrass)
		foxEat(fox, visibleRabbits)

	#If no visible grass, move randomly
	else:
		moveRandomly(fox)

def foxEat(fox, visibleRabbits):
	nearestRabbit = visibleRabbits[0]
	for rabbit in visibleRabbits: 
		#just start with the closest grass being the first visible one
		nearestRabbitDistance = math.sqrt((nearestRabbit.pos[0] - fox.pos[0])**2 + (nearestRabbit.pos[1] - fox.pos[1])**2)
		newDistance = math.sqrt((rabbit.pos[0] - fox.pos[0])**2 + (rabbit.pos[1] - fox.pos[1])**2)
		if(newDistance < nearestRabbitDistance):
			nearestRabbit = rabbit
			nearestRabbitDistance = newDistance
	
	#Move towards nearest grass
	theta = math.atan2(nearestRabbit.pos[1] - fox.pos[1], nearestRabbit.pos[0] - fox.pos[0])
	#had to scale it up a little with * 1.5
	dx = fox.velocity * math.cos(theta) * 1.5
	dy = fox.velocity * math.sin(theta) * 1.5

	fox.pos = (fox.pos[0] + int(dx), fox.pos[1] + int(dy))

	#check if a rabbit has reached the nearest piece of food and update stats/delete piece of food
	if(nearestRabbitDistance < 10):
		if(fox.hunger + 50.0 > 100.0):	
			fox.hunger = 100.0
		else:
			fox.hunger += 50.0
		rabbitList.remove(nearestRabbit)
		#print("Reached rabbit")

def foxFuck(fox, visibleMates):
	nearestMate = visibleMates[0]
	for mate in visibleMates: 
		nearestMateDistance = math.sqrt((nearestMate.pos[0] - fox.pos[0])**2 + (nearestMate.pos[1] - fox.pos[1])**2)
		newDistance = math.sqrt((mate.pos[0] - fox.pos[0])**2 + (mate.pos[1] - fox.pos[1])**2)
		if(newDistance < nearestMateDistance):
			nearestMate = mate
			nearestMateDistance = newDistance
	
	#Move towards nearest grass
	theta = math.atan2(nearestMate.pos[1] - fox.pos[1], nearestMate.pos[0] - fox.pos[0])
	#had to scale it up a little with * 1.5
	dx = fox.velocity * math.cos(theta) * 1.5
	dy = fox.velocity * math.sin(theta) * 1.5
	fox.pos = (fox.pos[0] + dx, fox.pos[1] + dy)

	if(int(nearestMateDistance) < 10):
		fox.timeOfLastFuck = 0.0
		nearestMate.timeOfLastFuck = 0.0
		#Make them have sex and spawn a new fox by averaging the stats of the parental foxes
		foxList.append(Fox(fox.pos, (fox.size+nearestMate.size)//2, 50, random.randint(0, 360)))
		#print("Reached fox mate")

def foxSeekMate(fox):
	#print("searching for mate")
	visibleMates = []
	#Check if any potential mates are within your vision
	for foxB in foxList:
		#Only go to mate if they're also looking for a mate
		if(foxB.hunger > 50 and foxB.timeOfLastFuck > 0.01):
			#Dont check yourself
			if(foxB != fox):
				distance = math.sqrt((foxB.pos[0] - fox.pos[0])**2 + (foxB.pos[1] - fox.pos[1])**2)
				if(distance <= fox.searchRadius):
					#print("See a mate")
					visibleMates.append(foxB)

	#If no visible mates, move randomly
	if(len(visibleMates) == 0):
		moveRandomly(fox)
	#If there are visible mates, find the closest one and move towards it
	else:
		foxFuck(fox, visibleMates)

def boundaryCheck(animal, dx, dy):
	
	x = animal.pos[0]
	y = animal.pos[1]

	#If not in range rotate theta by 90
	if(math.sqrt((x-canvasWidth/2+dx)**2 + (y-canvasHeight/2+dy)**2) > spawnRadius):
		animal.theta += 90
		animal.timeOfLastRotation = clock.time()
		animal.timeBeforeRotate = random.uniform(3, 6)
	else:
		animal.pos = (animal.pos[0] + dx, animal.pos[1] + dy)
