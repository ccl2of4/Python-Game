import pygame
import constants
import math

class EntityDelegate :
	def get_all_entities (self) :
		pass
	def spawn_entity (self, entity) :
		pass
	def despawn_entity (self, entity) :
		pass

class Entity (pygame.sprite.Sprite) :
	def __init__ (self,x=0, y=0,width=0,height=0,**images) :
		pygame.sprite.Sprite.__init__ (self)
		self.images = images
		self.width = width
		self.height = height
		self.physical = True
		self.affected_by_gravity = True
		self.velocity = (0,0)
		self.grounded = False
		self.sliding = True
		self.delegate = None
		self.image = None
		self.update_image ()
		self.rect = self.image.get_rect ()
		self.rect.move_ip (x,y)
		self.pass_through_entities = []
		self.friendly_entities = []

	def get_delegate (self) :
		return self.delegate
	def set_delegate (self, delegate) :
		self.delegate = delegate

	def is_grounded (self) :
		return self.grounded

	def is_physical (self) :
		return self.physical
	def set_physical (self, physical) :
		self.physical = physical

	def is_affected_by_gravity (self) :
		return self.affected_by_gravity
	def set_affected_by_gravity (self, affected_by_gravity) :
		self.affected_by_gravity = affected_by_gravity

	#entities that this entity should pass through without touching
	def get_pass_through_entities (self) :
		return self.pass_through_entities
	def set_pass_through_entities (self, pass_through_entities) :
		self.pass_through_entities = pass_through_entities

	#entities that this entity should not harm
	def get_friendly_entities (self) :
		return self.friendly_entities
	def set_friendly_entities (self, friendly_entities) :
		self.friendly_entities = friendly_entities

	def was_attacked (self, knockback) :
		pass

	def update (self) :

		v_x = self.velocity[0]
		v_y = self.velocity[1]
		self.grounded = False

		entities = self.delegate.get_all_entities ()

		if self.affected_by_gravity :
			v_y += constants.gravity

		if self.physical :

			#apply friction and test for collisions
			for entity in entities :
				if (entity is self 
					or entity in self.pass_through_entities 
					or self in entity.pass_through_entities) :
					continue

				touching = get_touching (self.rect, entity.rect)

				if Location.above == touching :
					self.grounded = True
					if self.sliding : 
						v_x *= .9
				elif Location.below == touching :
					if self.sliding :
						v_x *= .9
				elif Location.left == touching :
					pass
				elif Location.right == touching :
					pass

			target_rect = self.rect.move (v_x, v_y)
			union_rect = self.rect.union (target_rect)

			for entity in entities :
				if (entity is self 
					or entity in self.pass_through_entities 
					or self in entity.pass_through_entities) :
					continue

				#this means velocity vector will cause an interection with the current entity
				if union_rect.colliderect (entity.rect) :
					location_before = get_location (self.rect, entity.rect)
					location_after = get_location (target_rect, entity.rect)

					if location_before & Location.left :
						v_x = min (v_x, entity.rect.left - self.rect.right)
					elif location_before & Location.right :
						v_x = max (v_x, entity.rect.right - self.rect.left)

					if location_before & Location.above :
						v_y = min (v_y, entity.rect.top - self.rect.bottom)
					elif location_before & Location.below :
						v_y = max (v_y, entity.rect.bottom - self.rect.top)

		if self.grounded :
			self.grounded = abs (v_y) == 0 #won't be grounded for next update if you're leaving the ground
			#if you leave the ground horizontally that would also cause a problem

		self.velocity = v_x, v_y
		self.rect.move_ip (*self.velocity)
		self.update_image ()

	def update_image (self) :
		if self.image == None :
			self.image = pygame.image.load (self.images['default'])
		if self.width != 0 or self.height != 0 :
			self.image = pygame.transform.scale (self.image, (self.width,self.height))

class Location :
	none = 0
	above = 2 << 0
	below = 2 << 1
	left = 2 << 2
	right = 2 << 3
	inside = 3 << 4

#additional pygame.Rect utility functions
def get_location (rect1, rect2) :
	result = 0
	if (rect1.right <= rect2.left) :
		result += Location.left
	if (rect1.left >= rect2.right) :
		result += Location.right
	if (rect1.top >= rect2.bottom) :
		result += Location.below
	if (rect1.bottom <= rect2.top) :
		result += Location.above
	return result

def get_touching (rect1, rect2) :
	if (rect1.right == rect2.left and (rect1.bottom > rect2.top and rect1.top < rect2.bottom)) :
		return Location.right
	if (rect1.left == rect2.right and (rect1.bottom > rect2.top and rect1.top < rect2.bottom)) :
		return Location.left
	if (rect1.top == rect2.bottom and (rect1.right > rect2.left and rect1.left < rect2.right)) :
		return Location.below
	if (rect1.bottom == rect2.top and (rect1.right > rect2.left and rect1.left < rect2.right)) :
		return Location.above
	if (rect1.colliderect(rect2)) :
		return Location.inside
	return Location.none