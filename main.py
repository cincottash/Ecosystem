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

	populateCanvas(10, 40)
	
	drawSprites()

	while time < 0.01:
		#reset background
		canvas.fill(WHITE)

		drawSprites()

		update()
		
		print(time)

		rabbitPop.append(len(rabbitList))
		timeStamps.append(time*10000)

		#commit changes
		pygame.display.update()

	plotStuff()
	
def update():
	global time
	
	print(time)

	updateRabbitStuff()

	updateGrassStuff()

	time += dt
	clock.sleep(.05)

if __name__== '__main__':
	main()