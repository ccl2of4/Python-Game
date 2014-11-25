import pygame
import constants
from Entity import EntityDelegate
from Camera import Camera

class Game (EntityDelegate) :
	def __init__(self, width, height, camera=None) :
		pygame.init()
		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock ()
		self.all_entities = pygame.sprite.Group ()
		self.all_controllers = []
		self.camera = camera

	def add_entity (self, entity) :
		self.all_entities.add (entity)

	def add_controller (self, controller) :
		self.all_controllers.append (controller)

	def get_camera (self) :
		return self.camera
	def set_camera (self, camera) :
		self.camera = camera

	def set_main_entity (self, entity) :
		self.camera.set_target (entity)

	def run (self) :
		while 1:
			self.clock.tick (60)
			
			for controller in self.all_controllers :
				controller.update ()

			self.all_entities.update ()

			self.camera.update ()
			for entity in self.all_entities :
				self.camera.apply (entity)

			self.screen.fill (constants.background_color)
			self.all_entities.draw (self.screen)
			pygame.display.flip ()
			pygame.event.pump ()

	def get_all_entities (self) :
		return self.all_entities