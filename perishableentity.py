from entity import Entity
from lifecontroller import LifeControllerClient
from lifecontroller import LifeController
from notificationcenter import NotificationCenter

global perishable_entity_died_notification
perishable_entity_died_notification = 'perishable entity died notification'

class PerishableEntity (Entity, LifeControllerClient) :
	def __init__ (self, pos=(0,0), **images) :
		Entity.__init__ (self, pos,**images)
		self._life_controller = None
		self.set_life_controller (LifeController ())


	def life_controller_client_died (self) :
		NotificationCenter.shared_center().post_notification (self, perishable_entity_died_notification)
		self._delegate.despawn_entity (self)

	#the life controller that monitors this entity's life
	def get_life_controller (self) :
		return self._life_controller
	def set_life_controller (self, life_controller) :
		if self._life_controller :
			self._life_controller.set_client (None)
		if life_controller :
			life_controller.set_client (self)
		self._life_controller = life_controller

	def was_attacked (self, knockback, damage) :
		Entity.was_attacked (self, knockback, damage)
		if self._life_controller != None :
			self._life_controller.receive_damage (damage)