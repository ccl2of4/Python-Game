from entity import *
import pygame

class CompositeEntity (Entity) :
	def __init__ (self, pos = (0,0)) :
		Entity.__init__ (self, pos)
		self._inner_entities = None

	def get_description (self) :
		return "Composite Entity"

	def get_inner_entities (self) :
		return self._inner_entities
	def set_inner_entities (self, inner_entities) :

		rects = [entity.rect for entity in inner_entities]
		self.rect = rects[0].unionall (rects)
		self.rect.x, self.rect.y = self._pos[0], self._pos[1]
		print self.rect
		self._inner_entities = inner_entities

	def update_image (self) :
		self.image = pygame.Surface (self.rect.size)
		self.image.fill ((100,100,100))
		for entity in self._inner_entities :
			entity.update ()
			self.image.blit (entity.image, entity.rect)