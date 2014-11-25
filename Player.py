import pygame

import constants
from Entity import *
from Projectile import Projectile

global jump_accel
jump_accel = -15

global walk_accel
walk_accel = 1.0

global terminal_walk_velocity
terminal_walk_velocity = 8

global run_velocity_factor
run_velocity_factor = 2

global run_accel_factor
run_accel_factor = 2

global running_anim_duration
running_anim_duraction = 5

global walking_anim_duration
walking_anim_duration = 10

class Player (Entity) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :

		#used for animation
		self.walking = False
		self.running = False
		self.jumping = False
		self.running_duration = 0
		self.walking_duration = 0

		#can't call init before we know which image we're going to use
		Entity.__init__ (self,x,y,width,height,**images)

	def update (self) :	
		
		#slow the character if not inputing anything
		if not self.walking and not self.running :
			self.velocity = self.velocity[0]*.99, self.velocity[1]
		
		Entity.update (self)
		
		#reset all bools for the next update
		self.sliding = True
		self.running = False
		self.walking = False
		self.jumping = False

	def update_image (self) :
		direction = self.direction

		should_use_running_anim = self.running
		should_use_walking_anim = self.walking
		should_use_standing_anim = True

		if self.jumping :
			if direction == Direction.left :
				self.image = pygame.image.load (self.images['jump_left'])
			else :
				self.image = pygame.image.load (self.images['jump_right'])
			should_use_running_anim = False
			should_use_walking_anim = False
			should_use_standing_anim = False

		if should_use_running_anim :
			self.running_duration += 1
			if (self.running_duration < running_anim_duraction) :
				if direction == Direction.left :
					self.image = pygame.image.load (self.images['run_left'])
				else :
					self.image = pygame.image.load (self.images['run_right'])
				should_use_walking_anim = False
				should_use_standing_anim = False

		if should_use_walking_anim :
			self.walking_duration += 1
			if (self.walking_duration < walking_anim_duration) :
				if direction == Direction.left :
					self.image = pygame.image.load (self.images['walk_left'])
				else :
					self.image = pygame.image.load (self.images['walk_right'])
				should_use_standing_anim = False

		if should_use_standing_anim :
			if self.direction == Direction.left :
				self.image = pygame.image.load (self.images['stand_left'])
			else :
				self.image = pygame.image.load (self.images['stand_right'])

		if self.running_duration > 2*running_anim_duraction :
			self.running_duration = 0

		if self.walking_duration > 2*walking_anim_duration :
			self.walking_duration = 0

		Entity.update_image (self)



	def look_right (self) :
		self.direction = Direction.right
	def look_left (self) :
		self.direction = Direction.left

	def jump (self) :
		self.jumping = True
		if self.grounded:
			self.velocity = self.velocity[0], self.velocity[1] + jump_accel
		else :
			self.velocity = self.velocity[0], self.velocity[1] - 0.35*constants.gravity

	def walk (self, running) :
		self.sliding = False
		self.running = running
		self.walking = not running
		accel = self.horizontal_acceleration ()
		self.velocity = self.velocity[0] + accel, self.velocity[1]

	def shoot (self) :
		if self.weapon != None :
			self.weapon.fire ()

	def attack (self) :
		entities = self.delegate.get_all_entities ()
		for entity in entities :
			touching = get_touching (self.rect, entity.rect)
			if touching == Location.right and self.direction == Direction.right :
				entity.was_attacked ((20,-10))
			elif touching == Location.left and self.direction == Direction.left :
				entity.was_attacked((-20,-10))

	def was_attacked (self, knockback) :
		self.velocity = self.velocity[0] + knockback[0], self.velocity[1] + knockback[1]

	def found_weapon (self, weapon) :
		if self.weapon == None :
			self.weapon = weapon
			weapon.owner = self

	def horizontal_acceleration (self) :
		assert (self.walking or self.running)

		v_x = self.velocity[0]
		accel = walk_accel
		term_vel = terminal_walk_velocity

		if self.running :
			accel *= run_accel_factor
			term_vel *= run_velocity_factor

		if v_x > 0 :
			if self.direction == Direction.right :
				return max (0, accel - v_x/term_vel * accel)
			else :
				return -accel
		else :
			if self.direction == Direction.left :
				return min (0, -accel + v_x/term_vel * -accel)
			else :
				return accel

