import pygame
from entity import *

class UserInputEntityController (EntityController) :
	def __init__ (self) :
		
		self._walking = False
		self._running = False
		self._jumping = False
		self._w_attacking = False
		self._attacking = False
		self._dropping = False
		self._entity = None

		self._drop_needs_reset = False
		self._jump_needs_reset = False
		self._w_attack_needs_reset = False
		self._attack_needs_reset = False

	def update (self, entity) :
		if self._entity == None :
			self._entity = entity
		else :
			assert (entity == self._entity)

		keys = pygame.key.get_pressed ()

		self._walking = False
		self._running = False
		self._jumping = False
		self._w_attacking = False
		self._attacking = False
		self._dropping = False
		self._picking_up = False
		self._interacting = False

		#walk
		if keys[pygame.K_a] :
			self._entity.set_direction (Direction.left)
			self._walking = True
		elif keys[pygame.K_d] :
			self._entity.set_direction (Direction.right)
			self._walking = True
		
		#run
		if keys[pygame.K_s] :
			self._running = True

		#jump
		if keys[pygame.K_SPACE] :
			self._jumping = True
		elif self._entity.is_grounded ():
			self._jump_needs_reset = False

		#interact
		if keys[pygame.K_w] :
			self._interacting = True
		else :
			self._interacting = False

		#attack with weapon
		if keys[pygame.K_o] :
			self._w_attacking = True

		#pick up weapon
		if keys[pygame.K_p] :
			self._picking_up = True

		#drop weapon
		if keys[pygame.K_l] :
			self._dropping = True
		else :
			self._drop_needs_reset = False

		#attack
		if keys[pygame.K_i] :
			self._attacking = True
		else :
			self._attack_needs_reset = False



		#do the actions
		if self._walking :
			self._entity.walk (self._running)

		if self._jumping :
			if self._entity.is_grounded () and not self._jump_needs_reset :
				self._entity.jump ()
				self._jump_needs_reset = True
			elif not self._entity.is_grounded () :
				self._entity.jump ()

		if self._picking_up :
			self._entity.find_weapon ()

		if self._dropping :
			if not self._drop_needs_reset :
				self._entity.drop_weapon ()
				self._drop_needs_reset = True

		if self._interacting :
			self._entity.find_interaction ()

		if self._w_attacking :
			if not self._w_attack_needs_reset :
				self._entity.begin_attacking_with_weapon ()
				self._w_attack_needs_reset = True
		else :
			if self._w_attack_needs_reset :
				self._entity.end_attacking_with_weapon ()
				self._w_attack_needs_reset = False
			if self._attacking :
				if not self._attack_needs_reset :
					self._entity.attack ()
					self._attack_needs_reset = True