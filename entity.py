import pygame
import resource


class Direction :
	left = 0
	right = 1

class EntityDelegate :
	def get_all_entities (self) :
		pass
	def spawn_entity (self, entity) :
		pass
	def despawn_entity (self, entity) :
		pass

class EntityController :
	def update (self, entity) :
		pass

class Entity (pygame.sprite.Sprite) :
	def __init__ (self, pos=(0,0), **images) :
		pygame.sprite.Sprite.__init__ (self)

		self._layer = 0
		self._pos = pos

		#instance variables
		self._direction = Direction.right
		self._physical = True

		self._controller = None
		self._delegate = None

		self._images = images
		self.image = pygame.Surface ((0,0))
		self.rect = pygame.Rect ( pos, (0,0) )
		self._anchor_points = {}

		self._pass_through_entities = []
		self._friendly_entities = []

	def get_pos (self) :
		return self.rect.x, self.rect.y
	def set_pos (self, pos) :
		self.rect.x, self.rect.y = pos

	#anchor points for animation, etc.
	def get_anchor_points (self) :
		return self._anchor_points
	def set_anchor_points (self, **anchor_points) :
		self._anchor_points = anchor_points

	def get_description (self) :
		return "Entity"

	#default value None
	def get_controller (self) :
		return self._controller
	def set_controller (self, controller) :
		self._controller = controller

	#default value None
	def get_delegate (self) :
		return self._delegate
	def set_delegate (self, delegate) :
		self._delegate = delegate

	#does the entity collide with other entities?
	def is_physical (self) :
		return self._physical
	def set_physical (self, physical) :
		self._physical = physical

	#which direction is the entity facing?
	#irrelevant for some entities, but probably useful for most
	def get_direction (self) :
		return self._direction
	def set_direction (self, direction) :
		self._direction = direction

	#entities that this entity should pass through without touching
	def get_pass_through_entities (self) :
		return self._pass_through_entities
	def set_pass_through_entities (self, pass_through_entities) :
		self._pass_through_entities = pass_through_entities

	#entities that this entity should not harm
	def get_friendly_entities (self) :
		return self._friendly_entities
	def set_friendly_entities (self, friendly_entities) :
		self._friendly_entities = friendly_entities

	#is this entity able to collide with the given entity?
	def _can_collide_with_entity (self, entity) :
		return (entity is not self 
				and self.is_physical ()
				and entity.is_physical ()
				and not (entity in self._pass_through_entities) 
				and not (self in entity._pass_through_entities))

	#called when the entity is attacked by another entity
	#	can be refined in subclasses
	#	default implementation only looks at knockback
	def was_attacked (self, knockback, damage) :
		pass

	#can be overriden in subclasses
	#this code should be called anyway though
	def update (self) :
		if self._controller != None :
			self._controller.update (self)
		self.update_image ()
		rect = self.image.get_rect ()
		self.rect.width, self.rect.height = rect.width, rect.height

	#called after update
	#can be overridden. if the a subclass wishes to allow image scaling,
	#	it should call scale_image afterward
	def update_image (self) :
		key = self._images['default']
		self.image = resource.get_image (key)
		if self._direction == Direction.left :
			key += 'flip'
			if resource.has_image (key) :
				self.image = resource.get_image (key)
			else :
				self.image = pygame.transform.flip (self.image, True, False).convert ()
				resource.set_image (key, self.image)
		self.image.set_colorkey ((255,255,255))

#############################################
#additional utility functions for pygame.Rect
#############################################

#an enum for bit-masking
class Location :
	none = 0
	above = 2 << 0
	below = 2 << 1
	left = 2 << 2
	right = 2 << 3
	inside = 3 << 4

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