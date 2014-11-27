from Entity import *

class Explosion (Entity) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		self.knockback_factor = 10
		self.damage_factor = 10
		self.frames_to_live = 60
		self.alive_frames = 0

		Entity.__init__ (self,x,y,width,height,**images)

		self.set_physical (False)
		self.set_gravity (0)

	def get_knockback_factor (self) :
		return self.get_knockback_factor
	def set_knockback_factor (self, set_knockback_factor) :
		self.knockback_factor = knockback_factor

	def get_damage_factor (self) :
		return self.damage_factor
	def set_damage_factor (self, damage_factor) :
		self.damage_factor = damage_factor

	def get_frames_to_live (self) :
		return self.frames_to_live
	def set_frames_to_live (self, frames_to_live) :
		self.frames_to_live = frames_to_live

	def update (self) :
		self.alive_frames += 1
		if self.alive_frames > self.frames_to_live :
			self.delegate.despawn_entity (self)

		center = self.rect.center

		for entity in self.delegate.get_all_entities () :
			if (entity in self.friendly_entities
				or entity in self.pass_through_entities) :
				continue

			touching = get_touching (self.rect, entity.rect)
			if (touching == Location.none) :
				continue

			e_center = entity.rect.center

			if center[0] < e_center[0] :
				k_x = self.knockback_factor
			else :
				k_x = -self.knockback_factor

			if center[1] > e_center[1] :
				k_y = -self.knockback_factor
			else :
				k_y = self.knockback_factor

			damage = self.damage_factor

			entity.was_attacked ((k_x, k_y), damage)

		Entity.update (self)

	def update_image (self) :
		self.image = pygame.Surface ((self.width, self.height))
		self.image.fill ((255,0,0))
		self.image.set_alpha (255 - 255*self.alive_frames/self.frames_to_live)

		Entity.update_image (self)