from entity import *
from moveableentity import MoveableEntity

class Weapon (MoveableEntity) :

	def __init__ (self, pos = (0,0), **images) :
		MoveableEntity.__init__ (self, pos,**images)

		self._layer = 10

		self.set_physical (True)
		self.set_gravity (1.0)
		self._owner = None
		self._name = "Weapon"

	#attacking has begin/end state instead of just being called so that things
	#	like automatic gunfine can be implemented
	def begin_attacking (self) :
		pass
	def end_attacking (self) :
		pass

	#the owner should be invulnerable to any entities
	#created by the weapon
	def get_owner (self) :
		return self._owner

	def drop (self, drop_rect) :

		self.set_physical (True)

		can_be_dropped = True
		for entity in self._delegate.get_all_entities () :
			if self._can_collide_with_entity (entity) :
				touching = get_touching (drop_rect, entity.rect)
				if touching != Location.none :
					can_be_dropped = False
					break

		if not can_be_dropped :
			self.set_physical (False)
			return False

		self.rect = drop_rect
		self.set_gravity (1.0)
		self._owner = None
		return True

	def pick_up (self, owner) :
		if self._owner != None :
			return False
		self._velocity = (0,0)
		self.set_physical (False)
		self.set_gravity (0.0)
		self._owner = owner
		return True

	def update (self) :
		MoveableEntity.update (self)