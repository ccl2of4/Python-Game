from entity import *
from weapon import Weapon
from projectile import Projectile
from explosion import Explosion

class Bomb (Weapon, Projectile) :
	def __init__(self,x=0,y=0,width=10,height=10, **images) :
		Weapon.__init__ (self,x,y,width,height,**images)
		Projectile.__init__ (self,x,y,width,height,**images)
		self.has_been_launched = False
		self.set_knockback_factor (5)
		self.damage = 5

	def get_description (self) :
		return "Bomb"

	def attack (self) :
		v_x, v_y = 0, 0
		if self.owner != None :

			#make sure bomb doesn't hurt its owner
			self.friendly_entities.append (self.owner)
			self.pass_through_entities.append (self.owner)

			if self.owner.direction == Direction.right :
				v_x = 10.0
			else :
				v_x = -10.0
			v_y = -10.0

			#this call creates a circular dependency between bomb and character, and I don't like it
			#	also there's a bug if the owner cannot drop the weapon
			self.owner.drop_weapon ()

		self.launch ((v_x,v_y))

	def drop (self, drop_rect) :
		if self.has_been_launched :
			return False
		return Weapon.drop (self, drop_rect)

	def pick_up (self, owner) :
		if self.has_been_launched :
			return False
		return Weapon.pick_up (self, owner)

	def launch (self, velocity) :
		Projectile.launch (self, velocity)
		self.has_been_launched = True

	def made_contact (self, entity) :
		#spawn an explosion
		explosion = Explosion (self.rect.centerx, self.rect.centery, 80, 80)
		explosion.rect.center = self.rect.center
		for entity in self.friendly_entities :
			explosion.friendly_entities.append (entity)
		for entity in self.pass_through_entities :
			explosion.pass_through_entities.append (entity)
		self.delegate.spawn_entity (explosion)

	def update (self) :
		if self.has_been_launched :
			Projectile.update (self)
		else :
			Weapon.update (self)

	def calculate_knockback (self, entity) :
		touching = get_touching (self.rect, entity.rect)
		
		assert (touching != Location.none)

		f = self.get_knockback_factor ()

		if self.rect.center[0] < entity.rect.center[0] :
			k_x = f
		else :
			k_x = -f

		if self.rect.center[1] < entity.rect.center[1] :
			k_y = f
		else :
			k_y = -f
		
		return (k_x, k_y)