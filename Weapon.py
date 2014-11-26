from Entity import *

class Weapon (Entity) :

	def __init__ (self,x=0,y=0,width=0,height=0, **images) :
		Entity.__init__ (self,x,y,width,height,**images)
		self.set_physical (True)
		self.set_gravity (1.0)
		self.owner = None

	#override in subclasses
	def attack (self) :
		pass

	#the owner should be invulnerable to any entities
	#created by the weapon
	def get_owner (self) :
		return self.owner

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
		if self.owner == None :			
			entities = self.delegate.get_all_entities ()
			for entity in entities :
				touching = get_touching (entity.rect, self.rect)
				if touching :
					entity.found_weapon (self)

		Entity.update (self)