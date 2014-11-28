from Entity import Entity
from LifeController import LifeControllerClient
from LifeController import LifeController
import NotificationCenter

global perishable_entity_died_notification
perishable_entity_died_notification = 'perishable entity died notification'

class PerishableEntity (Entity, LifeControllerClient) :
	def __init__ (self,x=0,y=0,width=46,height=80, **images) :
		self.life_controller = None
		self.set_life_controller (LifeController ())
		Entity.__init__ (self,x,y,width,height,**images)


	def life_controller_client_died (self) :
		NotificationCenter.shared_center().post_notification (self, perishable_entity_died_notification)
		self.delegate.despawn_entity (self)

	#the life controller that monitors this entity's life
	def get_life_controller (self) :
		return self.life_controller
	def set_life_controller (self, life_controller) :
		if self.life_controller :
			self.life_controller.set_client (None)
		if life_controller :
			life_controller.set_client (self)
		self.life_controller = life_controller

	def was_attacked (self, knockback, damage) :
		Entity.was_attacked (self, knockback, damage)
		if self.life_controller != None :
			self.life_controller.receive_damage (damage)