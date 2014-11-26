from EntityController import EntityController
from Entity import *

class AIEntityController (EntityController) :
	def __init__ (self, entity) :
		EntityController.__init__ (self, entity)
		self.target_entity = None

	def get_target_entity (self) :
		return self.target_entity
	def set_target_entity (self, target_entity) :
		self.target_entity = target_entity

	def update (self) :
		if self.target_entity.rect.center > self.entity.rect.center :
			self.entity.set_direction (Direction.right)
		else :
			self.entity.set_direction (Direction.left)

		self.entity.walk (False)