import random
import math
import time as clock

from globals import *
from rabbit import *
from grass import *
from fox import *

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
				rabbitList.append(Rabbit((x, y), size))
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
				foxList.append(Fox((x, y), size))
				placed = 1
				currentFoxPop += 1


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

		#Prioritize running from foxes over eating and fucking
		if(checkForPredators(rabbit) == False):
		#If not hungry and havent fucked in a while check for a mate
			if (rabbit.hunger > 50 and rabbit.timeSinceLastFuck > 0.01):
				rabbitSeekMate(rabbit)
			#Search for food if hungry
			elif(rabbit.hunger <= 50):
				# #Search through grass within searchspawnRadius
				rabbitForage(rabbit)
			#If not hungry just move randomly
			else:
				moveRandomly(rabbit)

	#divide by zero check
	# try:
	# 	averageRabbitSize.append(rabbitSizes/len(rabbitList))
	# except ZeroDivisionError:
	# 	print("WARNING: All rabbits are dead")

def updateGrassStuff(time1):
	#Handle grass regrowth
	currentTime = time1
	#print(int(currentTime*10000.0 % 30))
	if(int(currentTime*100000.0) % 300 == 0.0 and int(currentTime*10000.0) > 0.0):
		#print("placing grass at %s" % currentTime)
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

	#Should make a random angle as well
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
	dx = rabbit.velocity * math.cos(theta) * 1.5
	dy = rabbit.velocity * math.sin(theta) * 1.5
	rabbit.pos = (rabbit.pos[0] + int(dx), rabbit.pos[1] + int(dy))

	if(int(nearestMateDistance) < 10):
		rabbit.timeSinceLastFuck = 0.0
		nearestMate.timeSinceLastFuck = 0.0
		#Make them have sex and spawn a new rabbit by averaging the stats of the parental rabbits
		rabbitList.append(Rabbit(rabbit.pos, int((rabbit.size+nearestMate.size)/2)))
		print("Reached mate")

def rabbitForage(rabbit):
	#Search through grass within searchspawnRadius
	visibleGrass = []
	for grass in grassList:
		#Accounts for circle spawnRadius, not just the center coords
		distance = math.sqrt((grass.pos[0] - rabbit.pos[0])**2 + (grass.pos[1] - rabbit.pos[1])**2)-(grass.size + rabbit.size)
		#find closest grass within search area
		if(distance <= rabbit.searchspawnRadius):
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
		if(distance <= rabbit.searchspawnRadius):
			print("Spotted Fox!!!")
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
		#had to scale it up a little with * 1.5
		dx = rabbit.velocity * math.cos(theta) * -1.5
		dy = rabbit.velocity * math.sin(theta) * -1.5

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
		if(rabbitB.hunger > 50 and rabbitB.timeSinceLastFuck > 0.01):
			#Dont check yourself
			if(rabbitB != rabbit):
				distance = math.sqrt((rabbitB.pos[0] - rabbit.pos[0])**2 + (rabbitB.pos[1] - rabbit.pos[1])**2)-(rabbitB.size + rabbit.size)
				if(distance <= rabbit.searchspawnRadius):
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
		
		fox.timeSinceLastFuck += dt
		
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
		if (fox.hunger > 50 and fox.timeSinceLastFuck > 0.01):
			#rabbitSeekMate(rabbit)
			print("Looking for mate")
			
			foxSeekMate(fox)
		#Search for food if hungry
		elif(fox.hunger <= 50):
			#Search through grass within searchspawnRadius
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
	#Search through grass within searchspawnRadius
	visibleRabbits = []
	for rabbit in rabbitList:
		#Accounts for circle spawnRadius, not just the center coords
		distance = math.sqrt((rabbit.pos[0] - fox.pos[0])**2 + (rabbit.pos[1] - fox.pos[1])**2)
		#find closest grass within search area
		if(distance <= fox.searchspawnRadius):
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
		print("Reached rabbit")

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
	fox.pos = (fox.pos[0] + int(dx), fox.pos[1] + int(dy))

	if(int(nearestMateDistance) < 10):
		fox.timeSinceLastFuck = 0.0
		nearestMate.timeSinceLastFuck = 0.0
		#Make them have sex and spawn a new rabbit by averaging the stats of the parental rabbits
		foxList.append(Fox(fox.pos, int((fox.size+nearestMate.size)/2)))
		print("Reached fox mate")

def foxSeekMate(fox):
	#print("searching for mate")
	visibleMates = []
	#Check if any potential mates are within your vision
	for foxB in foxList:
		#Only go to mate if they're also looking for a mate
		if(foxB.hunger > 50 and foxB.timeSinceLastFuck > 0.01):
			#Dont check yourself
			if(foxB != fox):
				distance = math.sqrt((foxB.pos[0] - fox.pos[0])**2 + (foxB.pos[1] - fox.pos[1])**2)
				if(distance <= fox.searchspawnRadius):
					#print("See a mate")
					visibleMates.append(foxB)

	#If no visible mates, move randomly
	if(len(visibleMates) == 0):
		moveRandomly(fox)
	#If there are visible mates, find the closest one and move towards it
	else:
		foxFuck(fox, visibleMates)

#THIS GETS STUCK WHEN IN CORNER OR RIGHT SIDE OF SCREEN
def boundaryCheck(animal, dx, dy):
	
	#Possible that x is not within the bounds but y is
	if(animal.pos[0] + dx  > maxCanvasWidth and (maxCanvasHeight < animal.pos[1] + dy < maxCanvasHeight)):
		animal.pos = (maxCanvasWidth, animal.pos[1] + animal.velocity*-1.5)
	#check the other end of the values
	elif(animal.pos[0] + dx  < minCanvasWidth and (minCanvasHeight < animal.pos[1] + dy < maxCanvasHeight)):
		animal.pos = (minCanvasWidth, animal.pos[1] + animal.velocity*-1.5)
	#Also possible that the x values are within screen range but the y values are not
	elif(minCanvasWidth < animal.pos[0] + dx < maxCanvasWidth and (animal.pos[1] + dy > maxCanvasHeight)):
		animal.pos = (animal.pos[0] + animal.velocity*-1.5, maxCanvasHeight)
	#check the other end of values
	elif(minCanvasWidth < animal.pos[0] + dx < maxCanvasWidth and (animal.pos[1] + dy < minCanvasHeight)):
		animal.pos = (animal.pos[0] + animal.velocity*-1.5, minCanvasHeight)
	#Currently they dont move when in a corner
	elif(animal.pos[0] + dx > maxCanvasWidth or animal.pos[0] + dx < minCanvasWidth):
		if(animal.pos[1] + dy > maxCanvasHeight or animal.pos[1] + dy < minCanvasHeight):
			animal.pos = (animal.pos[0], animal.pos[1])
	else:
		animal.pos = (animal.pos[0] + dx, animal.pos[1] + dy)