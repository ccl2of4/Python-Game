import pygame
from entity import *
from moveableentity import MoveableEntity

class Projectile (MoveableEntity) :
	def __init__ (self, pos = (0,0), **images) :
		MoveableEntity.__init__ (self, pos,**images)
		self._frames_to_live = 60
		self._knockback_factor = 1.0
		self._damage = 0

	#launch the projectile
	#in most cases, this should be called immediately after spawning into the game
	def launch (self, velocity) :
		self._velocity = velocity

	#how much knockback does this projectile transfer to its target?
	#knockback is handled differently between Projectile subclasses, so this
	#	scalar is simply used to denote how powerful the projectile should be
	def get_knockback_factor (self) :
		return self._knockback_factor
	def set_knockback_factor (self, knockback_factor) :
		self._knockback_factor = knockback_factor

	#how much damage does this projectile transfer to its target?
	def get_damage (self) :
		return self._damage
	def set_damage (self, damage) :
		self._damage = damage

	#overriden by subclasses to calculate the knockback that this projectile should apply to
	#	the given entity
	def _calculate_knockback (self, entity) :
		pass

	#how many screen updates does this projectile have before it despawns?
	def get_frames_to_live (self) :
		return self._frames_to_live
	def set_frames_to_live (self, frames_to_live) :
		self._frames_to_live = frames_to_live

	def update (self) :
		self._frames_to_live -= 1
		if self._frames_to_live < 0 :
			self._delegate.despawn_entity (self)

		MoveableEntity.update (self)

		#check if projectile made contact after the update
		entities = self._delegate.get_all_entities ()
		for entity in entities :
			if not self._can_collide_with_entity (entity) :
				continue

			touching = get_touching (self.rect, entity.rect)

			if touching == Location.none :
				continue

			v_x, v_y = self._calculate_knockback (entity)

			if not (entity in self._friendly_entities) :
				entity.was_attacked ((v_x,v_y), self._damage)

			self._made_contact (entity)

			self._delegate.despawn_entity (self)

	#do anything else after making contact with an
	#	entity. Projectile is despawned immediately after
	#	this method returns
	def _made_contact (self, entity) :
		pass
