import pygame
import constants

class Game :
	def __init__(self) :
		pygame.init()
		self.screen = pygame.display.set_mode((constants.window_width, constants.window_height))
		self.clock = pygame.time.Clock ()
		self.all_entities = pygame.sprite.Group ()

	def add_entity (self,entity) :
		self.all_entities.add (entity)

	def run (self) :
		while 1:
			self.clock.tick (60)
			
			self.all_entities.update ()

			#collision detection
			for entity in self.all_entities :
				for other_entity in self.all_entities :
					if entity is other_entity :
						continue
					if entity.rect.colliderect (other_entity.rect) :
						entity.did_collide (other_entity)
						other_entity.did_collide (entity)

			self.screen.fill (constants.background_color)
			self.all_entities.draw (self.screen)
			pygame.display.flip ()
			pygame.event.pump ()