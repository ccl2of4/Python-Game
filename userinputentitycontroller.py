import pygame
from entitycontroller import EntityController
from entity import *

class UserInputEntityController (EntityController) :
	def __init__ (self, entity) :
		EntityController.__init__ (self,entity)
		
		self.walking = False
		self.running = False
		self.jumping = False
		self.w_attacking = False
		self.attacking = False
		self.dropping = False
		self.delegate = None

		self.drop_needs_reset = False
		self.jump_needs_reset = False
		self.w_attack_needs_reset = False
		self.attack_needs_reset = False

	def get_delegate (self) :
		return self.delegate
	def set_delegate (self, delegate) :
		self.delegate = delegate

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

		#drop weapon
		if keys[pygame.K_i] :
			self.dropping = True
		else :
			self.drop_needs_reset = False

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
			if not self.drop_needs_reset :
				self.entity.drop_weapon ()
				self.drop_needs_reset = True

		if self.w_attacking :
			if not self.w_attack_needs_reset :
				self.entity.begin_attacking_with_weapon ()
				self.w_attack_needs_reset = True
		else :
			if self.w_attack_needs_reset :
				self.entity.end_attacking_with_weapon ()
				self.w_attack_needs_reset = False
			if self.attacking :
				if not self.attack_needs_reset :
					self.entity.attack ()
					self.attack_needs_reset = True