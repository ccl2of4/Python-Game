import pygame
from entity import *
from moveableentity import MoveableEntity

class Projectile (MoveableEntity) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		MoveableEntity.__init__ (self,x,y,width,height,**images)
		self.frames_to_live = 60
		self.knockback_factor = 1.0
		self.damage = 0

	#launch the projectile
	#in most cases, this should be called immediately after spawning into the game
	def launch (self, velocity) :
		self.velocity = velocity

	#how much knockback does this projectile transfer to its target?
	#knockback is handled differently between Projectile subclasses, so this
	#	scalar is simply used to denote how powerful the projectile should be
	def get_knockback_factor (self) :
		return self.knockback_factor
	def set_knockback_factor (self, knockback_factor) :
		self.knockback_factor = knockback_factor

	#how much damage does this projectile transfer to its target?
	def get_damage (self) :
		return self.damage
	def set_damage (self, damage) :
		self.damage = damage

	#overriden by subclasses to calculate the knockback that this projectile should apply to
	#	the given entity
	def calculate_knockback (self, entity) :
		pass

	#how many screen updates does this projectile have before it despawns?
	def get_frames_to_live (self) :
		return self.frames_to_live
	def set_frames_to_live (self, frames_to_live) :
		self.frames_to_live = frames_to_live

	def update (self) :
		self.frames_to_live -= 1
		if self.frames_to_live < 0 :
			self.delegate.despawn_entity (self)

		MoveableEntity.update (self)

		#check if projectile made contact after the update
		entities = self.delegate.get_all_entities ()
		for entity in entities :
			if not self.can_collide_with_entity (entity) :
				continue

			touching = get_touching (self.rect, entity.rect)

			if touching == Location.none :
				continue

			v_x, v_y = self.calculate_knockback (entity)

			if not (entity in self.friendly_entities) :
				entity.was_attacked ((v_x,v_y), self.damage)

			self.made_contact (entity)

			self.delegate.despawn_entity (self)

	#do anything else after making contact with an
	#	entity. Projectile is despawned immediately after
	#	this method returns
	def made_contact (self, entity) :
		pass
