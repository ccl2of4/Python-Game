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
	def __init__(self, pos = (0,0), **images) :
		Weapon.__init__ (self, pos,**images)
		self._firing_velocity = 20
		self._magazine = []
		self._cooldown = 30
		self._name = "Firearm"

		#used for timing
		self._cooldown_frames_left = 0

	def get_description (self) :
		result = self._name + " ("
		if len (self._magazine) > 0 :
			result += self._magazine[0].get_description () + " x" + str (len (self._magazine))
		else :
			result += "Empty"
		result += ")"

		return result

	#load the gun with ammo (projectiles)
	def get_magazine (self) :
		return self._magazine
	def set_magazine (self, magazine) :
		self._magazine = magazine

	#how long do you have to wait before shooting again?
	def get_cooldown (self) :
		return self._cooldown
	def set_cooldown (self, cooldown) :
		self._cooldown = cooldown

	#hold down the trigger
	def begin_attacking (self) :

		#can't attack if still in cooldown
		if self._cooldown_frames_left > 0 :
			return

		self._fire ()

	#release the trigger
	def end_attacking (self) :
		pass

	def _fire (self) :

		assert ('muzzle' in self._anchor_points)

		point = self._anchor_points['muzzle']
		if self._direction == Direction.left :
			point = (self.rect.width - point[0], point[1])
		
		point = self.rect.x + point[0], self.rect.y + point[1]

		#unload a projectile from the magazine (if there are any) and fire
		if len (self._magazine) == 0 :
			NotificationCenter.shared_center().post_notification (self, firearm_out_of_ammo_notification)
			return

		projectile = self._magazine.pop(0)

		v_y = 0
		if (self._direction == Direction.right) :
			v_x = self._firing_velocity
		else :
			v_x = -self._firing_velocity

		projectile.rect.center = point
		projectile.set_direction (self._direction)
		projectile.set_pass_through_entities ([self, self._owner])
		projectile.set_friendly_entities ([self, self._owner])
		self._delegate.spawn_entity (projectile)
		projectile.launch ((v_x,v_y))

		#cooldown before firing again
		self._cooldown_frames_left = self._cooldown

	#how quickly does a bullet shot from this gun travel?
	def get_firing_velocity (self) :
		return self._firing_velocity
	def set_firing_velocity (self, firing_velocity) :
		self._firing_velocity = firing_velocity

	def update (self) :
		assert (self._cooldown_frames_left >= 0)

		if self._cooldown_frames_left > 0 :
			self._cooldown_frames_left -= 1

		Weapon.update (self)
