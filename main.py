import pygame
import random
import math
from globals import *
from rabbit import *

pygame.init()

canvas = pygame.display.set_mode((canvasWidth, canvasHeight))

rabbitList = []

def main():

	populateCanvas(25)

	while True:
		canvas.fill((255,255,255))

		for rabbit in rabbitList:
			pygame.draw.circle(canvas, rabbit.color, rabbit.pos , rabbit.size)

		pygame.display.update()


def populateCanvas(initialRabbitPop):
	currentRabbitPop = 0

	while(currentRabbitPop < initialRabbitPop):
		placed = 0
		while(placed == 0):
			#Create a random set of cords and a randium size
			x = random.randint(canvasWidth/4, 3*canvasWidth/4)
			y = random.randint(canvasHeight/4, 3*canvasHeight/4)
			size = random.randint(6, 10)


			if(len(rabbitList) == 0):
					rabbitList.append(Rabbit((0,0,255), (x, y), size))
					placed = 1
					currentRabbitPop += 1
			else:
				canPLace = 1
				for rabbit in rabbitList:
					distance = math.sqrt((rabbit.pos[0]-x)**2 + (rabbit.pos[1]-y)**2)
					if(distance <= rabbit.size+size):
						print("overlap")
						placed = 0
						canPLace = 0
						break	
				
				if(canPLace):
					rabbitList.append(Rabbit((0,0,255), (x, y), size))
					placed = 1
					currentRabbitPop += 1
				


		



if __name__== '__main__':
	main()