from Controller import Controller
from Entity import *

class AIController (Controller) :
	def __init__ (self, entity) :
		Controller.__init__ (self, entity)
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