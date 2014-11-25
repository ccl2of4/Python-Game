import pygame
import constants
from Entity import EntityDelegate

class Game (EntityDelegate) :
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

			self.screen.fill (constants.background_color)
			self.all_entities.draw (self.screen)
			pygame.display.flip ()
			pygame.event.pump ()

	def get_all_entities (self) :
		return self.all_entities