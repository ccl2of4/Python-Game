from entity import *
from weapon import Weapon
from projectile import Projectile
from explosion import Explosion

class Bomb (Weapon, Projectile) :
	def __init__(self, pos = (0,0), **images) :
		Projectile.__init__ (self, pos, **images)
		Weapon.__init__ (self, pos, **images)
		self._has_been_launched = False
		self.set_knockback_factor (5)
		self._damage = 5
		self._name = "Bomb"

	def begin_attacking (self) :
		v_x, v_y = 0, 0
		if self._owner != None :

			#make sure bomb doesn't hurt its owner
			self._friendly_entities.append (self._owner)
			self._pass_through_entities.append (self._owner)

			if self._owner._direction == Direction.right :
				v_x = 10.0
			else :
				v_x = -10.0
			v_y = -10.0

			#this call creates a circular dependency between bomb and character, and I don't like it
			#	also there's a bug if the owner cannot drop the weapon
			self._owner.drop_weapon ()

		self.launch ((v_x,v_y))

	def end_attacking (self) :
		pass

	def drop (self, drop_rect) :
		if self._has_been_launched :
			return False
		return Weapon.drop (self, drop_rect)

	def pick_up (self, owner) :
		if self._has_been_launched :
			return False
		return Weapon.pick_up (self, owner)

	def launch (self, velocity) :
		Projectile.launch (self, velocity)
		self._has_been_launched = True

	def _made_contact (self, entity) :
		#spawn an explosion
		explosion = Explosion (default='images/explosion.png')
		explosion.set_pos ( (self.rect.centerx - 50, self.rect.centery - 50) )
		for entity in self._friendly_entities :
			explosion._friendly_entities.append (entity)
		for entity in self._pass_through_entities :
			explosion._pass_through_entities.append (entity)
		self._delegate.spawn_entity (explosion)

	def update (self) :
		if self._has_been_launched :
			Projectile.update (self)
		else :
			Weapon.update (self)

	def _calculate_knockback (self, entity) :
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