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
	def set_owner (self, owner) :
		if owner != None :
			self.set_physical (False)
			self.set_gravity (0)
		else :
			self.set_physical (True)
			self.set_gravity (1.0)
		self.owner = owner
	def get_owner (self) :
		return self.owner

	def update (self) :
		if self.owner == None :			
			entities = self.delegate.get_all_entities ()
			for entity in entities :
				touching = get_touching (entity.rect, self.rect)
				if touching :
					entity.found_weapon (self)

		Entity.update (self)