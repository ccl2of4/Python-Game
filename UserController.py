import pygame
from Controller import Controller

class UserController (Controller) :
	def __init__ (self, entity) :
		Controller.__init__ (self,entity)
		
		self.walking = False
		self.running = False
		self.jumping = False
		self.shooting = False
		self.attacking = False

		self.jump_needs_reset = False
		self.shoot_needs_reset = False
		self.attack_needs_reset = False

	def update (self) :
		keys = pygame.key.get_pressed ()

		self.walking = False
		self.running = False
		self.jumping = False
		self.shooting = False
		self.attacking = False

		#walk
		if keys[pygame.K_a] :
			self.entity.look_left ()
			self.walking = True
		elif keys[pygame.K_d] :
			self.entity.look_right ()
			self.walking = True
		
		#run
		if keys[pygame.K_s] :
			self.running = True

		#jump
		if keys[pygame.K_SPACE] :
			self.jumping = True
		else :
			self.jump_needs_reset = False

		#shoot
		if keys[pygame.K_p] :
			self.shooting = True
		else :
			self.shoot_needs_reset = False

		#attack
		if keys[pygame.K_o] :
			self.attacking = True
		else :
			self.attack_needs_reset = False




		#do the actions
		if self.walking :
			self.entity.walk (self.running)

		if self.jumping :
			if self.entity.is_grounded () and not self.jump_needs_reset :
				self.entity.jump ()
				self.jump_needs_reset = True
			elif not self.entity.is_grounded () :
				self.entity.jump ()

		if self.shooting :
			if not self.shoot_needs_reset :
				self.entity.shoot ()
				self.shoot_needs_reset = True
		elif self.attacking : #can't attack and shoot at the same time
			if not self.attack_needs_reset :
				self.entity.attack ()
				self.attack_needs_reset = True