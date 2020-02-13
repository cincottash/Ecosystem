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
		elif(rabbit.hunger < 50):
			pygame.draw.circle(canvas, RED, (int(rabbit.pos[0]), int(rabbit.pos[1])), rabbit.size)
		#Not hungry
		else:
			red = int(255 - (((rabbit.hunger-50)/50)*255))
			green = int(0)
			blue = int(((rabbit.hunger-50)/50)*255)
		
			pygame.draw.circle(canvas, (red, green, blue), (int(rabbit.pos[0]), int(rabbit.pos[1])), rabbit.size)
	
	for grass in grassList:
		pygame.draw.circle(canvas, grass.color, grass.pos, grass.size)

	for fox in foxList:
		if(rabbit.hunger == 0.0):
			pygame.draw.circle(canvas, BLACK, (int(rabbit.pos[0]), int(rabbit.pos[1])), rabbit.size)
		#if just hungry, completly red
		elif(rabbit.hunger < 50):
			pygame.draw.rect(canvas, RED, (fox.pos[0], fox.pos[1], fox.size, fox.size))
		#Not hungry
		else:
			red = int(255 - (((rabbit.hunger-50)/50)*255))
			green = int(0)
			blue = int(((rabbit.hunger-50)/50)*255)
			pygame.draw.rect(canvas, (red, blue, green), (fox.pos[0], fox.pos[1], fox.size, fox.size))
			


		