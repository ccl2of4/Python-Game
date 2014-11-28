import pygame
from Entity import EntityDelegate
from Camera import Camera
from NotificationCenter import NotificationCenter
import Character
import NotificationCenter
import Gun

class Positioning :
	absolute = 0
	relative = 1

class Game (EntityDelegate) :
	def __init__(self, width=800, height=400, camera=None) :
		pygame.init()
		self.last_update_time = pygame.time.get_ticks ()
		self.time_since_last_update = 0
		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock ()
		self.all_entities = pygame.sprite.OrderedUpdates ()
		self.all_controllers = []
		self.camera = camera
		self.log_message = None
		self.log_message_duration = None
		self.in_settings = False

		#settings stuff
		self.settings_button_needs_reset = False

		#register for notifications
		notification_names = self.get_notification_names ()
		for notification_name in notification_names :
			NotificationCenter.shared_center().add_observer (self, notification_name)

	def notify (self, poster, notification_name, **info) :
		main_entity = self.get_main_entity ()
		if Character.character_cannot_drop_weapon_notification == notification_name and poster == main_entity:
			self.log ("Cannot drop weapon here")
		elif Character.character_died_notification == notification_name :
			if poster == self.get_main_entity () :
				self.log ("You lost!")
			else :
				pass
		elif Character.character_picked_up_weapon_notification == notification_name and poster == main_entity :
			self.log (main_entity.get_weapon().get_description ())
		elif Gun.gun_out_of_ammo_notification == notification_name and poster.owner == main_entity :
			self.log ("Out of ammo!")

	def get_notification_names (self) :
		return [
			Character.character_cannot_drop_weapon_notification,
			Character.character_died_notification,
			Character.character_picked_up_weapon_notification,
			Gun.gun_out_of_ammo_notification
		]

	def add_controller (self, controller) :
		self.all_controllers.append (controller)

	def get_camera (self) :
		return self.camera
	def set_camera (self, camera) :
		self.camera = camera

	def get_main_entity (self) :
		return self.camera.get_target ()
	def set_main_entity (self, entity) :
		self.camera.set_target (entity)

	def log (self, message) :
		self.log_message = message
		self.log_message_duration = 0

	def run (self) :
		while 1:

			#framerate stuff
			self.clock.tick (60)

			#user input
			keys = pygame.key.get_pressed ()
			if keys[pygame.K_1] :
				if not self.settings_button_needs_reset :
					self.in_settings = not self.in_settings
					self.settings_button_needs_reset = True
			else :
				self.settings_button_needs_reset = False
			
			if self.in_settings :
				self.update_settings ()
			else :
				self.update_game ()


	def update_settings (self) :
			#rendering
			#self.screen.fill ((255,255,255))

			#pygame.display.flip ()
			pygame.event.pump ()


	def update_game (self) :
			#update controllers first, then entities
			for controller in self.all_controllers :
				controller.update ()
			self.all_entities.update ()

			
			#camera
			assert self.camera != None
			self.camera.update ()
			for entity in self.all_entities :
				if entity.positioning == Positioning.relative :
					self.camera.apply (entity)


			#rendering
			self.screen.fill ((255,255,255))
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
		entity.positioning = Positioning.relative
	def spawn_entity_absolute (self, entity) :
		self.all_entities.add (entity)
		entity.delegate = self	
		entity.positioning = Positioning.absolute
	def despawn_entity (self, entity) :
		self.all_entities.remove (entity)