import pygame

class UserController :
	def __init__ (self, entity) :
		self.entity = entity
		self.walking = False
		self.running = False
		self.jumping = False
		self.jump_needs_reset = False

	def update (self) :
		keys = pygame.key.get_pressed ()

		self.walking = False
		self.running = False
		self.jumping = False

		if keys[pygame.K_a] :
			self.entity.look_left ()
			self.walking = True
		elif keys[pygame.K_d] :
			self.entity.look_right ()
			self.walking = True
		else :
			self.walking = False
		if keys[pygame.K_w] :
			pass
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
		else :
			self.entity.idle ()

		if self.jumping :
			if self.entity.is_grounded () and not self.jump_needs_reset :
				self.entity.jump ()
				self.jump_needs_reset = True
			elif not self.entity.is_grounded () :
				self.entity.jump ()