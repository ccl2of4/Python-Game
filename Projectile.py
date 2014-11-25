from Entity import *

class Direction :
	left = 0
	right = 1

class Projectile (Entity) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		Entity.__init__ (self,x,y,width,height,**images)
		self.total_displacement = (0,0)
		self.despawn_distance = 500

	def update (self) :
		entities = self.delegate.get_all_entities ()
		for entity in entities :
			if (entity is self or
				entity in self.friendly_entities) :
				continue

			touching = get_touching (self.rect, entity.rect)

			if touching == Location.none :
				continue

			v_x, v_y = self.knockback

			if touching == Location.right :
				knockback = v_x, v_y
			elif touching == Location.left :
				knockback = -v_x, v_y
			elif touching == Location.above :
				knockback = v_x, -v_y
			elif touching == Location.below :
				knockback = v_x, v_y
			elif touching == Location.inside :
				knockback = v_x, v_y
			else :
				assert (False)

			entity.was_attacked (knockback)

			self.delegate.despawn_entity (self)

		Entity.update (self)

		self.total_displacement = self.total_displacement[0] + self.velocity[0], self.total_displacement[1] + self.velocity[1]
		if abs (self.total_displacement[0] + self.total_displacement[1]) > self.despawn_distance :
			self.delegate.despawn_entity (self)

	def get_shooter (self) :
		return self.shooter

	def get_knockback (self) :
		return self.knockback
	def set_knockback (self, knockback) :
		self.knockback = knockback

	def get_despawn_distance (self) :
		return self.despawn_distance
	def set_despawn_distance (self, despawn_distance) :
		self.despawn_distance = despawn_distance

	def set_shooter (self, shooter) :
		self.shooter = shooter
		self.friendly_entities = [shooter]
		self.pass_through_entities = [shooter]

	def update_image (self) :
		Entity.update_image (self)

	def fire (self, velocity) :
		self.velocity = velocity