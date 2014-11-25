import pygame

import constants
from Entity import *
from Projectile import Projectile

class Gun (Entity) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		Entity.__init__ (self,x,y,width,height,**images)
		self.set_physical (False)
		self.set_affected_by_gravity (False)
		self.owner = None

	def fire (self) :
		p_width = 5
		p_height = 5

		if self.direction == Direction.right :
			p_x = self.rect.right
		else :
			p_x = self.rect.left - p_width
		p_y = self.rect.center[1]

		v_y = 0
		if (self.direction == Direction.right) :
			v_x = 10
		else :
			v_x = -10

		knockback_x = 10
		if (v_x < 0) :
			knockback_x *= -1
		knockback_y = 0

		#make a projectile
		projectile = Projectile (p_x, p_y, p_width, p_height, default='images/platform.png')
		projectile.set_affected_by_gravity (False)
		projectile.set_pass_through_entities ([self, self.owner])
		projectile.set_friendly_entities ([self, self.owner])
		projectile.set_knockback ((knockback_x, knockback_y))
		self.delegate.spawn_entity (projectile)
		projectile.launch ((v_x,v_y))

	def get_direction (self) :
		return self.direction
	def set_direction (self) :
		self.direction = direction

	def get_owner (self) :
		return self.owner
	def set_owner (self, owner) :
		self.owner = owner

	def update (self) :

		if self.owner != None :
			self.velocity = (0,0)
			
			if self.owner.direction == Direction.left :
				x = self.owner.rect.left - self.rect.width
			else :
				x = self.owner.rect.right

			y = self.owner.rect.center[1]

			self.rect.x = x
			self.rect.y = y

			self.direction = self.owner.direction

		else :
			entities = self.delegate.get_all_entities ()
			for entity in entities :
				touching = get_touching (entity.rect, self.rect)
				if touching :
					entity.found_weapon (self)

		Entity.update (self)