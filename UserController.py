import pygame
from Controller import Controller
from Entity import *

class UserController (Controller) :
	def __init__ (self, entity) :
		Controller.__init__ (self,entity)
		
		self.walking = False
		self.running = False
		self.jumping = False
		self.w_attacking = False
		self.attacking = False
		self.dropping = False

		self.jump_needs_reset = False
		self.w_attack_needs_reset = False
		self.attack_needs_reset = False

	def update (self) :
		keys = pygame.key.get_pressed ()

		self.walking = False
		self.running = False
		self.jumping = False
		self.w_attacking = False
		self.attacking = False
		self.dropping = False

		#walk
		if keys[pygame.K_a] :
			self.entity.set_direction (Direction.left)
			self.walking = True
		elif keys[pygame.K_d] :
			self.entity.set_direction (Direction.right)
			self.walking = True
		
		#run
		if keys[pygame.K_s] :
			self.running = True

		#jump
		if keys[pygame.K_SPACE] :
			self.jumping = True
		else :
			self.jump_needs_reset = False

		#attack with weapon
		if keys[pygame.K_p] :
			self.w_attacking = True
		else :
			self.w_attack_needs_reset = False

		#drop weapon
		if keys[pygame.K_i] :
			self.dropping = True

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

		if self.dropping :
			self.entity.drop ()

		if self.w_attacking :
			if not self.w_attack_needs_reset :
				self.entity.attack_with_weapon ()
				self.w_attack_needs_reset = True
		elif self.attacking : #can't attack and shoot at the same time
			if not self.attack_needs_reset :
				self.entity.attack ()
				self.attack_needs_reset = True