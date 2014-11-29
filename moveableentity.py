from entity import *

class MoveableEntity (Entity) :
	def __init__ (self,x=0,y=0,width=46,height=80, **images) :
		Entity.__init__ (self,x,y,width,height,**images)
		self.velocity = (0,0)
		self.grounded = False
		self.sliding = True
		self.mass = 0
		self.gravity = 1.0

	def get_description (self) :
		return "Moveable Entity"

	#is the entity on top of another entity?
	def is_grounded (self) :
		return self.grounded

	#the mass of this entity, used for bouncing after collisions
	#	setting mass to 0 implies infinite mass
	#currently unused
	def get_mass (self) :
		return self.mass
	def set_mass (self, mass) :
		self.mass = mass

	#control how fast an entity sinks when free falling
	#setting to 0 effectively disables gravity on this entity
	def get_gravity (self) :
		return self.gravity
	def set_gravity (self, gravity) :
		self.gravity = gravity

	def was_attacked (self, knockback, damage) :
		Entity.was_attacked (self, knockback, damage)
		if self.mass > 0 :
			self.velocity = self.velocity[0] + knockback[0], self.velocity[1] + knockback[1]

	def update (self) :
		v_x = self.velocity[0]
		v_y = self.velocity[1]
		
		v_y += self.gravity

		#an optimization
		if v_y != 0 or v_x != 0 :
			entities = self.delegate.get_all_entities ()

			if self.physical :

				#apply friction
				for entity in entities :
					if not self.can_collide_with_entity (entity) :
						continue

					touching = get_touching (self.rect, entity.rect)

					if Location.above == touching :
						v_y = min (0, v_y)
						if self.sliding : 
							v_x *= .9
					elif Location.below == touching :
						v_y = max (0, v_y)
						if self.sliding :
							v_x *= .9
					elif Location.left == touching :
						v_x = max (0, v_x)
					elif Location.right == touching :
						v_x = min (0, v_x)


				#look out for collisions
				target_rect = self.rect.move (v_x, v_y)
				union_rect = self.rect.union (target_rect)
				for entity in entities :
					if not self.can_collide_with_entity (entity) :
						continue

					#this works well enough for now
					if union_rect.colliderect (entity.rect) :
						location_before = get_location (self.rect, entity.rect)
						location_after = get_location (target_rect, entity.rect)

						if location_before & Location.left :
							v_x = min (v_x, entity.rect.left - self.rect.right)
						elif location_before & Location.right :
							v_x = max (v_x, entity.rect.right - self.rect.left)
						elif location_before & Location.above :
							v_y = min (v_y, entity.rect.top - self.rect.bottom)
						elif location_before & Location.below :
							v_y = max (v_y, entity.rect.bottom - self.rect.top)

			#update the actual rect
			self.rect.move_ip (v_x, v_y)

			#update grounded
			if self.physical :
				self.grounded = False
				for entity in entities :
					if not self.can_collide_with_entity (entity) :
						continue
					touching = get_touching (self.rect, entity.rect)
					if Location.above == touching :
						self.grounded = True
						break

		#finally update velocity
		self.velocity = v_x, v_y

		Entity.update (self)
