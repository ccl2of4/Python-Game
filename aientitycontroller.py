from entitycontroller import EntityController
from entity import *
import random

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

		if random.randint (0,60) < 10 :
			self.entity.walk (False)
		if random.randint (0,60) == 1 :
			self.entity.attack ()
		if random.randint (0,1000) == 1 :
			self.entity.jump ()
		if random.randint (0,120) == 1 :
			self.entity.begin_attacking_with_weapon ()
			self.entity.end_attacking_with_weapon ()