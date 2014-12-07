from entity import *
import random


#just walks toward the target and does melee attacks
class ZombieEntityController (EntityController) :
	def __init__ (self) :
		self._target_entity = None
		self._entity = None

	def get_target_entity (self) :
		return self._target_entity
	def set_target_entity (self, target_entity) :
		self._target_entity = target_entity

	def update (self, entity) :
		if self._entity == None :
			self._entity = entity
		else :
			assert (entity == self._entity)

		if self._target_entity.rect.center > self._entity.rect.center :
			self._entity.set_direction (Direction.right)
		else :
			self._entity.set_direction (Direction.left)

		if random.randint (0,60) < 10 :
			self._entity.walk (False)
		if random.randint (0,60) == 1 :
			self._entity.attack ()

#walks toward the target and attacks
class SlayerEntityController (EntityController) :
	def __init__ (self) :
		self._target_entity = None
		self._entity = None

	def get_target_entity (self) :
		return self._target_entity
	def set_target_entity (self, target_entity) :
		self._target_entity = target_entity

	def update (self, entity) :
		if self._entity == None :
			self._entity = entity
		else :
			assert (entity == self._entity)

		if self._target_entity.rect.center > self._entity.rect.center :
			self._entity.set_direction (Direction.right)
		else :
			self._entity.set_direction (Direction.left)

		if self._entity.get_weapon () == None :
			self._entity.find_weapon ()

		if random.randint (0,60) < 10 :
			self._entity.walk (False)
		if random.randint (0,60) == 1 :
			self._entity.attack ()
		if random.randint (0,1000) == 1 :
			self._entity.jump ()
		if random.randint (0,120) == 1 :
			self._entity.begin_attacking_with_weapon ()
			self._entity.end_attacking_with_weapon ()