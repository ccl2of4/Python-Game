import pygame

class Player (pygame.sprite.Sprite) :
	def __init__(self) :
		pygame.sprite.Sprite.__init__ (self)
		self.image = pygame.image.load ('mariostand.png')
		self.rect = self.image.get_rect ()

	def update (self) :
		keys = pygame.key.get_pressed ()
		if keys[pygame.K_d] :
			self.rect.move_ip (1,0)
		if keys[pygame.K_w] :
			self.rect.move_ip (0,-1)
		if keys[pygame.K_s] :
			self.rect.move_ip (0,1)
		if keys[pygame.K_a] :
			self.rect.move_ip (-1,0)