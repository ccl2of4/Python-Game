import pygame

from Entity import *
from Projectile import Projectile

class Gun (Entity) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		Entity.__init__ (self,x,y,width,height,**images)
		self.set_physical (False)
		self.set_gravity (0)
		self.owner = None
		self.firing_velocity = 10

	def fire (self) :
		b_width = 5
		b_height = 5

		if self.direction == Direction.right :
			b_x = self.rect.right
		else :
			b_x = self.rect.left - b_width
		b_y = self.rect.center[1]

		v_y = 0
		if (self.direction == Direction.right) :
			v_x = self.firing_velocity
		else :
			v_x = -self.firing_velocity

		knockback_x = 10
		if (v_x < 0) :
			knockback_x *= -1
		knockback_y = 0

		#shoot a bullet
		bullet = Projectile (b_x, b_y, b_width, b_height, default='images/platform.png')
		bullet.set_gravity (0)
		bullet.set_pass_through_entities ([self, self.owner])
		bullet.set_friendly_entities ([self, self.owner])
		bullet.set_knockback ((knockback_x, knockback_y))
		self.delegate.spawn_entity (bullet)
		bullet.launch ((v_x,v_y))

	#the owner should be invulnerable to any bullets fired by the gun
	def get_owner (self) :
		return self.owner
	def set_owner (self, owner) :
		self.owner = owner

	#how quickly does a bullet shot from this gun travel?
	def get_firing_velocity (self) :
		return self.firing_velocity
	def set_firing_velocity (self, firing_velocity) :
		self.firing_velocity = firing_velocity

	def update (self) :
		if self.owner != None :
			self.velocity = (0,0)
			
			center = self.owner.get_weapon_rect_center ()
			direction = self.owner.get_direction ()

			self.set_direction (direction)
			self.rect.center = center

		else :
			entities = self.delegate.get_all_entities ()
			for entity in entities :
				touching = get_touching (entity.rect, self.rect)
				if touching :
					entity.found_weapon (self)

		Entity.update (self)
