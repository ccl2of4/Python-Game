import pygame
import constants
from Entity import EntityDelegate
from Camera import Camera

class Game (EntityDelegate) :
	def __init__(self, width, height, camera=None) :
		pygame.init()
		self.last_update_time = pygame.time.get_ticks ()
		self.time_since_last_update = 0
		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock ()
		self.all_entities = pygame.sprite.Group ()
		self.all_controllers = []
		self.camera = camera
		self.log_message = None
		self.log_message_duration = None

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

			#framerate stuff
			self.clock.tick (60)
			
			for controller in self.all_controllers :
				controller.update ()

			self.all_entities.update ()

			self.camera.update ()
			for entity in self.all_entities :
				self.camera.apply (entity)

			self.screen.fill (constants.background_color)
			self.all_entities.draw (self.screen)

			if self.log_message != None :
				percent = min (1.0, self.log_message_duration/60.0)
				if percent < 1 :
					font = pygame.font.Font (None, 36)
					text = font.render (self.log_message, 1, (percent*255, percent*255, percent*255))
					textpos = text.get_rect ()
					textpos.centerx = self.screen.get_rect().centerx
					self.screen.blit (text, textpos)
					self.log_message_duration += 1
				else :
					log_message = None

			pygame.display.flip ()
			pygame.event.pump ()

	
	#######################
	#EntityDelegate methods
	#######################

	def get_all_entities (self) :
		return self.all_entities

	def spawn_entity (self, entity) :
		self.all_entities.add (entity)
		entity.delegate = self

	def despawn_entity (self, entity) :
		self.all_entities.remove (entity)

	def log (self, message) :
		self.log_message = message
		self.log_message_duration = 0
