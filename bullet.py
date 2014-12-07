from entity import *
from projectile import Projectile

class Bullet (Projectile) :
	def __init__ (self, pos = (0,0), **images) :
		Projectile.__init__ (self, pos,**images)
		self.set_gravity (0)
		self.set_knockback_factor (5)
		self.set_damage (5)
		self._name = "Bullet"

	def _calculate_knockback (self, entity) :
		touching = get_touching (self.rect, entity.rect)
		assert (touching != Location.none)

		f = self.get_knockback_factor ()

		if Location.left == touching :
			return (-f,0)
		elif Location.right == touching :
			return (f,0)
		elif Location.above == touching :
			return (0,-f)
		elif Location.below == touching :
			return (0,f)
		elif Location.inside == touching :
			return (0,-f)
		
		assert (False)