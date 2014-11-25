import pygame

import constants
from Entity import Entity

global jump_accel
jump_accel = -10

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

class Direction :
	left = 0
	right = 1

class Player (Entity) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		self.walking = False
		self.running = False
		self.jumping = False
		self.direction = Direction.right
		self.running_duration = 0
		self.walking_duration = 0
		Entity.__init__ (self,x,y,width,height,**images)

	def update (self) :
		keys = pygame.key.get_pressed ()

		self.walking = False
		self.running = False
		self.jumping = False

		if keys[pygame.K_a] :
			self.walking = True
			self.direction = Direction.left
		elif keys[pygame.K_d] :
			self.walking = True
			self.direction = Direction.right
		else :
			self.walking = False
		if keys[pygame.K_w] :
			pass
		if keys[pygame.K_s] :
			self.running = self.walking #can't be running if you're not walking
			self.walking = False #can't be running AND walking
		else :
			self.running = False
		if keys[pygame.K_SPACE] :
			self.jumping = True

		if self.running or self.walking :
			self.move_horizontally ()
		else :
			self.idle ()
		
		if self.jumping :
			self.jump ()

		Entity.update (self)

	def update_image (self) :
		direction = self.direction

		should_use_walking_anim = self.walking
		should_use_standing_anim = True

		if self.running :
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

	def jump (self) :
		if self.grounded:
			self.velocity = self.velocity[0], self.velocity[1] + jump_accel
		else :
			self.velocity = self.velocity[0], self.velocity[1] - 0.25*constants.gravity

	def move_horizontally (self) :
		self.sliding = False
		accel = self.horizontal_acceleration ()
		self.velocity = self.velocity[0] + accel, self.velocity[1]

	def idle (self) :
		self.sliding = True
		self.velocity = self.velocity[0]*.99, self.velocity[1]

	def is_running (self) :
		return self.running

	def horizontal_acceleration (self) :
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

