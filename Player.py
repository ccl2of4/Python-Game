import pygame
from Entity import Entity

class Player (Entity) :
	def __init__(self, image) :
		Entity.__init__ (self,image)

	def update (self) :
		Entity.update (self)
		keys = pygame.key.get_pressed ()
		if keys[pygame.K_d] :
			self.rect.move_ip (1,0)
		if keys[pygame.K_w] :
			self.rect.move_ip (0,-1)
		if keys[pygame.K_s] :
			self.rect.move_ip (0,1)
		if keys[pygame.K_a] :
			self.rect.move_ip (-1,0)

	def did_collide (self, other) :
		Entity.did_collide (self, other)
