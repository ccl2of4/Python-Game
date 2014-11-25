from Entity import *

class Projectile (Entity) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		Entity.__init__ (self,x,y,width,height,**images)
		self.frames_to_live = 60

	def launch (self, velocity) :
		self.velocity = velocity

	def get_knockback (self) :
		return self.knockback
	def set_knockback (self, knockback) :
		self.knockback = knockback

	def get_frames_to_live (self) :
		return self.frames_to_live
	def set_frames_to_live (self, frames_to_live) :
		self.frames_to_live = frames_to_live

	def update (self) :
		
		self.frames_to_live -= 1
		if self.frames_to_live < 0 :
			self.delegate.despawn_entity (self)

		entities = self.delegate.get_all_entities ()
		for entity in entities :
			if (entity is self
				or entity in self.friendly_entities
				or entity in self.pass_through_entities
				or not entity.is_physical ()) :
				continue

			touching = get_touching (self.rect, entity.rect)

			if touching == Location.none :
				continue

			v_x, v_y = self.knockback

			entity.was_attacked (self.knockback)

			self.delegate.despawn_entity (self)

		Entity.update (self)

	def update_image (self) :
		Entity.update_image (self)