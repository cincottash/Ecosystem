import pygame
import random
import math
import time as clock

from globals import *
from rabbit import *
from grass import *
from plot import * 
from draw import *
from updateMethods import *
global time

def main():

	populateCanvas(12, 40, 4)
	
	drawSprites()

	while (time < maxTime):
		#reset background
		canvas.fill(WHITE)

		update()
		
		drawSprites()

		print(time)

		rabbitPop.append(len(rabbitList))
		
		timeStamps.append(time)
		
		#commit changes
		pygame.display.update()

	plotStuff()

	
def update():
	global time
	
	updateRabbitStuff()

	updateGrassStuff(time)

	updateFoxStuff()

	time += dt
	clock.sleep(.05)

if __name__== '__main__':
	main()