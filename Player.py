import pygame

from Entity import Entity

global jump_accel
jump_accel = -10

global walk_accel
walk_accel = 1

global terminal_walk_velocity
terminal_walk_velocity = 2

class Direction :
	left = 0
	right = 1

class Player (Entity) :
	def __init__(self, image) :
		Entity.__init__ (self,image)

	def update (self) :
		keys = pygame.key.get_pressed ()

		if keys[pygame.K_a] :
			self.direction = Direction.left
			self.walk ()
		if keys[pygame.K_d] :
			self.direction = Direction.right
			self.walk ()
		if keys[pygame.K_w] :
			pass
		if keys[pygame.K_s] :
			pass
		if keys[pygame.K_SPACE] :
			self.jump ()

		Entity.update (self)

	def jump (self) :
		if self.grounded:
			self.velocity = self.velocity[0], self.velocity[1] + jump_accel

	def get_direction (self) :
		return self.direction
	def set_direction (self, direction)	:
		self.direction = direction

	def walk (self) :
		pass

	def run (self) :
		pass

	def did_collide (self, other) :
		Entity.did_collide (self, other)
