from Entity import *
from Weapon import Weapon
from Projectile import Projectile

class Bomb (Weapon, Projectile) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		Weapon.__init__ (self,x,y,width,height,**images)
		Projectile.__init__ (self,x,y,width,height,**images)
		self.has_been_launched = False
		self.set_knockback_factor (10)

	def attack (self) :
		v_x, v_y = 0, 0
		if self.owner != None :
			if self.owner.direction == Direction.right :
				v_x = 10.0
			else :
				v_x = -10.0
			v_y = -10.0
			self.owner.drop_weapon ()
		self.launch ((v_x,v_y))

	def launch (self, velocity) :
		Projectile.launch (self, velocity)
		self.has_been_launched = True

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