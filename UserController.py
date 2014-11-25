import pygame
from Controller import Controller

class UserController (Controller) :
	def __init__ (self, entity) :
		Controller.__init__ (self,entity)
		self.walking = False
		self.running = False
		self.jumping = False
		self.attacking = False
		self.jump_needs_reset = False
		self.attack_needs_reset = False

	def update (self) :
		keys = pygame.key.get_pressed ()

		self.walking = False
		self.running = False
		self.jumping = False
		self.attacking = False



		if keys[pygame.K_a] :
			self.entity.look_left ()
			self.walking = True
		elif keys[pygame.K_d] :
			self.entity.look_right ()
			self.walking = True
		else :
			self.walking = False
		if keys[pygame.K_w] :
			self.attacking = True
		else :
			self.attack_needs_reset = False
		if keys[pygame.K_s] :
			self.running = True
		else :
			pass
		if keys[pygame.K_SPACE] :
			self.jumping = True
		else :
			self.jump_needs_reset = False




		if self.walking :
			self.entity.walk (self.running)

		if self.attacking :
			if not self.attack_needs_reset :
				self.entity.attack ()
				self.attack_needs_reset = True

		if self.jumping :
			if self.entity.is_grounded () and not self.jump_needs_reset :
				self.entity.jump ()
				self.jump_needs_reset = True
			elif not self.entity.is_grounded () :
				self.entity.jump ()