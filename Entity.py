import pygame
import constants

class Entity (pygame.sprite.Sprite) :
	def __init__ (self, image, x=0, y=0,width=0,height=0) :
		pygame.sprite.Sprite.__init__ (self)
		self.image = pygame.image.load (image)
		if width != 0 or height != 0 :
			self.image = pygame.transform.scale (self.image, (width,height))
		self.rect = self.image.get_rect ()
		self.rect.move_ip (x,y)
		self.physical = True
		self.affected_by_gravity = True
		self.velocity = (0,0)
		self.acceleration = (0,0)
		self.grounded = False
	
	def is_physical (self) :
		return self.physical
	def set_physical (self, physical) :
		self.physical = physical

	def is_affected_by_gravity (self) :
		return self.affected_by_gravity
	def set_affected_by_gravity (self, affected_by_gravity) :
		self.affected_by_gravity = affected_by_gravity

	def update (self) :
		if self.affected_by_gravity :
			self.acceleration = (0,constants.gravity)
			self.velocity = (self.velocity[0] + self.acceleration[0], self.velocity[1] + self.acceleration[1])
		if self.grounded :
			self.velocity = (self.velocity[0], 0)
		self.rect.move_ip (*self.velocity)

	def did_collide (self, other) :
		self.grounded = True