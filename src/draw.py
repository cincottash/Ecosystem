import pygame
from globals import *

pygame.init()
canvas = pygame.display.set_mode((canvasWidth, canvasHeight))

def drawSprites():
	
	for rabbit in rabbitList:
		#if starving, make it black
		if(rabbit.hunger == 0.0):
			pygame.draw.circle(canvas, BLACK, (int(rabbit.pos[0]), int(rabbit.pos[1])), rabbit.size)
		#if just hungry, completly red
		elif(rabbit.hunger < (rabbit.maxHunger)/2):
			pygame.draw.circle(canvas, RED, (int(rabbit.pos[0]), int(rabbit.pos[1])), rabbit.size)
		#Not hungry
		else:
			#red is 1 when current hunger = maxHunger/2, red is 0 when current hunger = maxHunger
			red = 255 - int((((rabbit.hunger- (rabbit.maxHunger/2) ) / (rabbit.maxHunger/2))* 255))
			green = 0
			#blue is 0 when current hunger = maxHunger/2, blue is 1 when current hunger = maxHunger
			blue = int((((rabbit.hunger - (rabbit.maxHunger/2) ) / (rabbit.maxHunger/2))* 255))
		
			pygame.draw.circle(canvas, (red, green, blue), (int(rabbit.pos[0]), int(rabbit.pos[1])), rabbit.size)
	
	for grass in grassList:
		pygame.draw.circle(canvas, grass.color, (int(grass.pos[0]), int(grass.pos[1])), grass.size)

	for fox in foxList:
		if(fox.hunger == 0.0):
			pygame.draw.rect(canvas, BLACK, (fox.pos[0], fox.pos[1], fox.size, fox.size))
		#if just hungry, completly red
		elif(fox.hunger < 50):
			pygame.draw.rect(canvas, RED, (fox.pos[0], fox.pos[1], fox.size, fox.size))
		#Not hungry
		else:
			red = int(255 - (((fox.hunger-50)/50)*255))
			green = int(0)
			blue = ((fox.hunger-50)/50)*255
			pygame.draw.rect(canvas, (red, green, blue), (fox.pos[0], fox.pos[1], fox.size, fox.size))
			


		