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

	populateCanvas(15, 25)

	while True:
		canvas.fill((255,255,255))

		drawSprites()

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

		
if __name__== '__main__':
	main()