import pygame
from Entity import *

class Projectile (Entity) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		Entity.__init__ (self,x,y,width,height,**images)
		self.frames_to_live = 60

	#launch the projectile
	#in most cases, this should be called immediately after spawning into the game
	def launch (self, velocity) :
		self.velocity = velocity

	#how much knockback does this projectile transfer to its target?
	def get_knockback (self) :
		return self.knockback
	def set_knockback (self, knockback) :
		self.knockback = knockback

	#how many screen updates does this projectile have before it despawns?
	def get_time_to_live (self) :
		return self.frames_to_live
	def set_time_to_live (self, frames_to_live) :
		self.frames_to_live = frames_to_live

	def update (self) :
		self.frames_to_live -= 1
		if self.frames_to_live < 0 :
			self.delegate.despawn_entity (self)

		entities = self.delegate.get_all_entities ()
		for entity in entities :
			if not self.can_collide_with_entity (entity) :
				continue

			touching = get_touching (self.rect, entity.rect)

			if touching == Location.none :
				continue

			v_x, v_y = self.knockback

			if not (entity in self.friendly_entities) :
				entity.was_attacked (self.knockback)

			self.delegate.despawn_entity (self)

		Entity.update (self)