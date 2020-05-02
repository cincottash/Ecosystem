import pygame
import random
import math
import sys

from globals import *
from rabbit import *
from grass import *
from plot import * 
from draw import *
from updateMethods import *
global time

def main():

	startTime = clock.time()

	if(len(sys.argv) != 3):
		print("Incorrect argument count. Correct usage is: InitialRabbitPop InitialGrassPop")
		exit(0)
	else:
		intialRabbitPop = int(sys.argv[1])
		intialGrassPop = int(sys.argv[2])

	populateCanvas(intialRabbitPop, intialGrassPop)

	#Use this later for graphing
	maxRabbitPop = intialRabbitPop

	while (True):
		#reset background
		canvas.fill(BLACK)

		

		pygame.draw.circle(canvas, BROWN, (canvasWidth//2, canvasHeight//2), spawnRadius)
		update(startTime)
		
		drawSprites()

		if(len(rabbitList) > maxRabbitPop):
			maxRabbitPop = len(rabbitList)

		rabbitPop.append(len(rabbitList))
		
		timeStamps.append(time)
		
		#commit changes
		pygame.display.update()


		for event in pygame.event.get():	
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					plotStuff(timeStamps[len(timeStamps) - 1], maxRabbitPop)
					exit(0)

	

	
def update(startTime):
	global time
	
	updateRabbitStuff()

	updateGrassStuff()

	time = int(clock.time() - startTime)
	#print(time)
if __name__== '__main__':
	main()