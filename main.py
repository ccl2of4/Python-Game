import sys, pygame, time
from Player import Player

pygame.init()

size = width, height = 500, 300 
speed = [1, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

player = Player ()
allsprites = pygame.sprite.RenderPlain (player)

clock = pygame.time.Clock ()

while 1:
	clock.tick (60)
	allsprites.update ()
	screen.fill (black)
	allsprites.draw (screen)
	pygame.display.flip ()
	pygame.event.pump ()
