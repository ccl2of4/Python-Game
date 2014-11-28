import pygame
import NotificationCenter
from Entity import *

global point_of_interest_reached_notification
point_of_interest_reached_notification = 'point of interest reached notification'

class PointOfInterest (Entity) :
	def __init__ (self,x=0, y=0,width=0,height=0,**images) :
		Entity.__init__ (self,x,y,width,height,**images)
		self.set_physical (False)
		self.set_gravity (0)

	#post notification if any other entity touches this entity
	def update (self) :
		for entity in self.delegate.get_all_entities () :
			if (entity != self) and get_touching (self.rect, entity.rect) == Location.inside :
				NotificationCenter.shared_center().post_notification (self, point_of_interest_reached_notification,entity=entity)

		Entity.update (self)