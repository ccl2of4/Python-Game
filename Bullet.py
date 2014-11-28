from Entity import *
from Projectile import Projectile

class Bullet (Projectile) :
	def __init__(self,x=0,y=0,width=5,height=5, **images) :
		Projectile.__init__ (self,x,y,width,height,**images)
		self.set_gravity (0)
		self.set_knockback_factor (5)
		self.damage = 5

	def get_description (self) :
		return "Bullet"

	def calculate_knockback (self, entity) :
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