import sys, pygame, time
import constants
from Player import Player
from Entity import Entity

pygame.init()

screen = pygame.display.set_mode((constants.window_width, constants.window_height))

player = Player ("mariostand.png")

platform = Entity ("platform.png",0,300,200,20)
platform.set_affected_by_gravity (False)

all_entities = pygame.sprite.RenderPlain (player,platform)


clock = pygame.time.Clock ()

while 1:
	clock.tick (60)

	all_entities.update ()

	#collision detection
	for entity in all_entities :
		for other_entity in all_entities :
			if entity is other_entity :
				continue
			if entity.rect.colliderect (other_entity.rect) :
				entity.did_collide (other_entity)
				other_entity.did_collide (entity)

	screen.fill (constants.background_color)
	all_entities.draw (screen)
	pygame.display.flip ()
	pygame.event.pump ()
