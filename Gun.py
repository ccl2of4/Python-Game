import pygame

from Entity import *
from Bullet import Bullet
from Weapon import Weapon
from ExplosiveBullet import ExplosiveBullet

class Gun (Weapon) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		Weapon.__init__ (self,x,y,width,height,**images)
		self.firing_velocity = 10
		self.magazine = []

	def get_description (self) :
		result = "Gun ("
		if len (self.magazine) > 0 :
			result += self.magazine[0].get_description () + " x" + str (len (self.magazine))
		else :
			result += "Empty"
		result += ")"

		return result

	#load the gun with ammo (projectiles)
	def get_magazine (self) :
		return self.magazine
	def set_magazine (self, magazine) :
		self.magazine = magazine

	#fire the gun
	def attack (self) :
		#unload a projectile from the magazine and fire
		if len (self.magazine) > 0 :
			projectile = self.magazine.pop(0)

			p_width = projectile.rect.width
			p_height = projectile.rect.height

			if self.direction == Direction.right :
				p_x = self.rect.right
			else :
				p_x = self.rect.left - p_width
			p_y = self.rect.center[1]

			v_y = 0
			if (self.direction == Direction.right) :
				v_x = self.firing_velocity
			else :
				v_x = -self.firing_velocity


			projectile.rect.x = p_x
			projectile.rect.y = p_y
			projectile.set_pass_through_entities ([self, self.owner])
			projectile.set_friendly_entities ([self, self.owner])
			self.delegate.spawn_entity (projectile)
			projectile.launch ((v_x,v_y))

	#how quickly does a bullet shot from this gun travel?
	def get_firing_velocity (self) :
		return self.firing_velocity
	def set_firing_velocity (self, firing_velocity) :
		self.firing_velocity = firing_velocity

	def update (self) :
		Weapon.update (self)
