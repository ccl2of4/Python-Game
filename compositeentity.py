import pygame
from entity import Entity

#a class used solely for the purpose of optimization

class CompositeEntity (Entity) :
	def __init__ (self, pos=(0,0)) :
		Entity.__init__ (self, pos)
		self._entities = None
		self._needs_update = True

	def get_entities (self) :
		return self._entities

	def set_entities (self, entities) :
		self.rect = None

		for entity in entities :
			entity.update_image ()
			rect = entity.image.get_rect ()
			rect.topleft = entity.rect.topleft

			if self.rect == None :
				self.rect = rect
			else :
				self.rect.union_ip (rect)

		self._needs_update = True
		self._entities = entities

	def update_image (self) :
		if not self._needs_update :
			return

		self.image = pygame.Surface (self.rect.size)
		self.image.set_colorkey ( (255,255,255) )
		self.image.fill ( (255,255,255) )
		for entity in self._entities :
			entity.update_image ()
			rect = entity.image.get_rect ()
			rect.x, rect.y = entity.rect.x - self.rect.x, entity.rect.y - self.rect.y

			self.image.blit (entity.image, rect)

		self._needs_update = False
