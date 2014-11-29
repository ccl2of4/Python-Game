from entity import *
from moveableentity import MoveableEntity

class Weapon (MoveableEntity) :

	def __init__ (self,x=0,y=0,width=0,height=0, **images) :
		MoveableEntity.__init__ (self,x,y,width,height,**images)
		self.set_physical (True)
		self.set_gravity (1.0)
		self.owner = None

	#attacking has begin/end state instead of just being called so that things
	#	like automatic gunfine can be implemented
	def begin_attacking (self) :
		pass
	def end_attacking (self) :
		pass

	#the owner should be invulnerable to any entities
	#created by the weapon
	def get_owner (self) :
		return self.owner

	def get_description (self) :
		return "Weapon"

	def drop (self, drop_rect) :

		self.set_physical (True)

		can_be_dropped = True
		for entity in self.delegate.get_all_entities () :
			if self.can_collide_with_entity (entity) :
				touching = get_touching (drop_rect, entity.rect)
				if touching != Location.none :
					can_be_dropped = False
					break

		if not can_be_dropped :
			self.set_physical (False)
			return False

		self.rect = drop_rect
		self.set_gravity (1.0)
		self.owner = None
		return True

	def pick_up (self, owner) :
		if self.owner != None :
			return False
		self.set_physical (False)
		self.set_gravity (0.0)
		self.owner = owner
		return True

	def update (self) :
		MoveableEntity.update (self)