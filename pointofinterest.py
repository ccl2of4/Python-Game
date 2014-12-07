import pygame
from notificationcenter import NotificationCenter
from entity import *

global point_of_interest_reached_notification
point_of_interest_reached_notification = 'point of interest reached notification'

class PointOfInterest (Entity) :
	def __init__ (self, pos = (0,0), size = (64,64)) :
		Entity.__init__ (self,pos)
		self.set_physical (False)
		self._size = size
		self._layer = -1
		self._needs_update = True

	#post notification if any other entity touches this entity
	def update (self) :
		for entity in self._delegate.get_all_entities () :
			if (entity != self) and get_touching (self.rect, entity.rect) == Location.inside :
				NotificationCenter.shared_center().post_notification (self, point_of_interest_reached_notification,entity=entity)

		Entity.update (self)

	def update_image (self) :
		if self._needs_update :
			self.image = pygame.Surface (self._size)
			self.image.fill ((0,255,0))
			self._needs_update = False