import pygame

from Entity import *
from Bullet import Bullet
from Weapon import Weapon

class Gun (Weapon) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		Weapon.__init__ (self,x,y,width,height,**images)
		self.firing_velocity = 10

	#fire the gun
	def attack (self) :
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

		#shoot a bullet
		bullet = Bullet (b_x, b_y, b_width, b_height, default='images/platform.png')
		bullet.set_pass_through_entities ([self, self.owner])
		bullet.set_friendly_entities ([self, self.owner])
		self.delegate.spawn_entity (bullet)
		bullet.launch ((v_x,v_y))


	#how quickly does a bullet shot from this gun travel?
	def get_firing_velocity (self) :
		return self.firing_velocity
	def set_firing_velocity (self, firing_velocity) :
		self.firing_velocity = firing_velocity

	def update (self) :
		Weapon.update (self)
