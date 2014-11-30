import pygame

from entity import *
from bullet import Bullet
from weapon import Weapon
from explosivebullet import ExplosiveBullet
from notificationcenter import NotificationCenter
import notificationcenter

global firearm_out_of_ammo_notification
firearm_out_of_ammo_notification = 'firearm out of ammo notification'

class Firearm (Weapon) :
	def __init__(self,x=0,y=0,width=50,height=5, **images) :
		Weapon.__init__ (self,x,y,width,height,**images)
		self.firing_velocity = 10
		self.magazine = []
		self.cooldown = 30

		#used for timing
		self.cooldown_frames_left = 0

	def get_description (self) :
		result = "Firearm ("
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

	#how long do you have to wait before shooting again?
	def get_cooldown (self) :
		return self.cooldown
	def set_cooldown (self, cooldown) :
		self.cooldown = cooldown

	#hold down the trigger
	def begin_attacking (self) :

		#can't attack if still in cooldown
		if self.cooldown_frames_left > 0 :
			return

		self.fire ()

	#release the trigger
	def end_attacking (self) :
		pass

	def fire (self) :

		assert ('muzzle' in self.anchor_points)

		point = self.anchor_points['muzzle']
		if self.direction == Direction.left :
			point = (self.rect.width - point[0], point[1])
		
		point = self.rect.x + point[0], self.rect.y + point[1]

		#unload a projectile from the magazine (if there are any) and fire
		if len (self.magazine) == 0 :
			NotificationCenter.shared_center().post_notification (self, firearm_out_of_ammo_notification)
			return

		projectile = self.magazine.pop(0)

		v_y = 0
		if (self.direction == Direction.right) :
			v_x = self.firing_velocity
		else :
			v_x = -self.firing_velocity

		projectile.rect.center = point
		projectile.set_pass_through_entities ([self, self.owner])
		projectile.set_friendly_entities ([self, self.owner])
		self.delegate.spawn_entity (projectile)
		projectile.launch ((v_x,v_y))

		#cooldown before firing again
		self.cooldown_frames_left = self.cooldown

	#how quickly does a bullet shot from this gun travel?
	def get_firing_velocity (self) :
		return self.firing_velocity
	def set_firing_velocity (self, firing_velocity) :
		self.firing_velocity = firing_velocity

	def update (self) :
		assert (self.cooldown_frames_left >= 0)

		if self.cooldown_frames_left > 0 :
			self.cooldown_frames_left -= 1

		Weapon.update (self)
