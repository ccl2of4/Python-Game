import pygame

from Entity import *
from Projectile import Projectile

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

		#default physics coefficients
		self.jump_acceleration = -15.0
		self.walk_acceleration = 1.0
		self.terminal_walk_velocity = 8.0
		self.run_acceleration_factor = 1.5
		self.run_terminal_velocity_factor = 1.5
		self.jump_slow_fall_factor = 0.35

		#can't call init before we know which image we're going to use
		Entity.__init__ (self,x,y,width,height,**images)


	###########################
	#phyics config
	###########################

	#how much acceleration does a jump give the player?
	def get_jump_acceleration (self) :
		return self.jump_acceleration
	def set_jump_acceleration (self, jump_acceleration) :
		self.jump_acceleration = jump_acceleration

	#maximum walking acceleration. decreases linearly as
	#speed approaches terminal walking velocity
	def get_walk_acceleration (self) :
		return self.walk_acceleration
	def set_walk_acceleration (self, walk_acceleration) :
		self.set_walk_acceleration = walk_acceleration

	#maximum speed at which the player can walk
	def get_terminal_walk_velocity (self) :
		return self.terminal_walk_velocity
	def set_terminal_walk_velocity (self, terminal_walk_velocity) :
		self.terminal_walk_velocity = terminal_walk_velocity

	#how much faster does the player accelerate when running?
	def get_run_acceleration_factor (self) :
		return self.run_acceleration_factor
	def set_run_acceleration_factor (self, run_acceleration_factor) :
		self.run_acceleration_factor = run_acceleration_factor

	#by how much does the terminal walking velocity increase when running?
	def get_run_terminal_velocity_factor (self) :
		return self.run_terminal_velocity_factor
	def set_run_terminal_velocity_factor (self, run_terminal_velocity_factor) :
		self.run_terminal_velocity_factor = run_terminal_velocity_factor

	#when attemping to jump while falling, the slow fall factor
	#	dampens acceleration due to gravity
	def get_jump_slow_fall_factor (self) :
		return self.jump_slow_fall_factor
	def set_jump_slow_fall_factor (self, jump_slow_fall_factor) :
		self.jump_slow_fall_factor = jump_slow_fall_factor


	##############
	#actions
	##############

	#make the player jump
	def jump (self) :
		self.jumping = True
		if self.grounded:
			self.velocity = self.velocity[0], self.velocity[1] + self.jump_acceleration
		else :
			self.velocity = self.velocity[0], self.velocity[1] - self.jump_slow_fall_factor*self.gravity

	#player advances horizontally in the direction it is facing
	def walk (self, running) :
		self.sliding = False
		self.running = running
		self.walking = not running
		accel = self.calculate_horizontal_acceleration ()
		self.velocity = self.velocity[0] + accel, self.velocity[1]

	#fire a weapon
	def shoot (self) :
		if self.weapon != None :
			self.weapon.fire ()

	#melee attack
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

	def get_weapon_rect_center (self) :
		if self.direction == Direction.left :
			x = self.rect.left
		else :
			x = self.rect.right
		y = self.rect.center[1]
		return (x,y)

	def found_weapon (self, weapon) :
		if self.weapon == None :
			self.weapon = weapon
			weapon.owner = self

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
			self.image = pygame.image.load (self.images['jump'])
			if direction == Direction.left :
				self.image = pygame.transform.flip (self.image, True, False)
			should_use_running_anim = False
			should_use_walking_anim = False
			should_use_standing_anim = False

		if should_use_running_anim :
			self.running_duration += 1
			if (self.running_duration < running_anim_duraction) :
				self.image = pygame.image.load (self.images['run'])
				if direction == Direction.left :
					self.image = pygame.transform.flip (self.image, True, False)
				should_use_walking_anim = False
				should_use_standing_anim = False

		if should_use_walking_anim :
			self.walking_duration += 1
			if (self.walking_duration < walking_anim_duration) :
				self.image = pygame.image.load (self.images['walk'])
				if direction == Direction.left :
					self.image = pygame.transform.flip (self.image, True, False)
				should_use_standing_anim = False

		if should_use_standing_anim :
			self.image = pygame.image.load (self.images['stand'])
			if self.direction == Direction.left :
				self.image = pygame.transform.flip (self.image, True, False)

		if self.running_duration > 2*running_anim_duraction :
			self.running_duration = 0

		if self.walking_duration > 2*walking_anim_duration :
			self.walking_duration = 0

		Entity.update_image (self)

	#how much should we accelerate horizontally?
	def calculate_horizontal_acceleration (self) :
		assert (self.walking or self.running)

		v_x = self.velocity[0]
		accel = self.walk_acceleration
		term_vel = self.terminal_walk_velocity

		if self.running :
			accel *= self.run_acceleration_factor
			term_vel *= self.run_terminal_velocity_factor

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

