import pygame
from notificationcenter import NotificationCenter
from entity import *

global point_of_interest_reached_notification
point_of_interest_reached_notification = 'point of interest reached notification'

class PointOfInterest (Entity) :
	def __init__ (self,x=0, y=0,width=0,height=0) :
		Entity.__init__ (self,x,y,width,height)
		self.set_physical (False)

	#post notification if any other entity touches this entity
	def update (self) :
		for entity in self.delegate.get_all_entities () :
			if (entity != self) and get_touching (self.rect, entity.rect) == Location.inside :
				NotificationCenter.shared_center().post_notification (self, point_of_interest_reached_notification,entity=entity)

		Entity.update (self)

	def update_image (self) :
		self.image = pygame.Surface ((self.width, self.height))
		self.image.fill ((0,255,0))
		self.scale_image ()