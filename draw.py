import pygame
from globals import *

pygame.init()
canvas = pygame.display.set_mode((canvasWidth, canvasHeight))

def drawSprites():
	for rabbit in rabbitList:
		
		red = 255 - ((rabbit.hunger/100)*255)
		green = 0
		blue = (rabbit.hunger/100)*255
		
		pygame.draw.circle(canvas, (red, green, blue), (int(rabbit.pos[0]), int(rabbit.pos[1])) , int(rabbit.size))

	for grass in grassList:
		pygame.draw.circle(canvas, grass.color, grass.pos, grass.size)