import pygame

from Entity import Entity

global jump_accel
jump_accel = -10

global walk_accel
walk_accel = 1.0

global terminal_walk_velocity
terminal_walk_velocity = 5

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
		self.direction = Direction.right
		self.running_duration = 0
		self.walking_duration = 0
		Entity.__init__ (self,x,y,width,height,**images)

	def update (self) :
		keys = pygame.key.get_pressed ()

		if keys[pygame.K_a] :
			self.walking = True
			self.direction = Direction.left
			self.walk ()
		elif keys[pygame.K_d] :
			self.walking = True
			self.direction = Direction.right
			self.walk ()
		else :
			self.walking = False
			self.idle ()
		if keys[pygame.K_w] :
			pass
		if keys[pygame.K_s] :
			self.running = self.walking
		else :
			self.running = False
		if keys[pygame.K_SPACE] :
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

	def walk (self) :
		accel = self.walking_acceleration ()
		self.velocity = self.velocity[0] + accel, self.velocity[1]

	def idle (self) :
		self.velocity = self.velocity[0]*.8, self.velocity[1]

	def is_running (self) :
		return self.running

	def walking_acceleration (self) :
		accel = walk_accel
		term_vel = terminal_walk_velocity
		if self.running :
			accel *= run_accel_factor
			term_vel *= run_velocity_factor

		v_x = self.velocity[0]
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

