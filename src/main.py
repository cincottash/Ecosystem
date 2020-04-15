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

	if(len(sys.argv) != 4):
		print("Incorrect argument count. Correct usage is: InitialRabbitPop InitialGrassPop InitialFoxPop")
		exit(0)
	else:
		intialRabbitPop = int(sys.argv[1])
		intialGrassPop = int(sys.argv[2])
		intialFoxPop = int(sys.argv[3])

	populateCanvas(intialRabbitPop, intialGrassPop, intialFoxPop)

	while (time < maxTime):
		#reset background
		canvas.fill(BLACK)

		pygame.draw.circle(canvas, BROWN, (canvasWidth//2, canvasHeight//2), spawnRadius)
		#1080x1000
		update()
		
		drawSprites()

		#print(time)

		rabbitPop.append(len(rabbitList))
		
		timeStamps.append(time)
		
		#commit changes
		pygame.display.update()

		for event in pygame.event.get():	
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					plotStuff()
					exit(0)

	

	
def update():
	global time
	
	updateRabbitStuff()

	updateGrassStuff()

	updateFoxStuff()

	time += dt
	clock.sleep(.05)

if __name__== '__main__':
	main()