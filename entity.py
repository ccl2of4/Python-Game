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
	def __init__ (self,x=0, y=0,width=0,height=0,**images) :
		pygame.sprite.Sprite.__init__ (self)

		self._layer = 0

		#instance variables
		self.direction = Direction.right
		self.images = images
		self.width = width
		self.height = height
		self.physical = True
		self.controller = None
		self.delegate = None
		self.image = None
		self.update_image ()
		self.rect = self.image.get_rect().move (x,y)
		self.pass_through_entities = []
		self.friendly_entities = []

	def get_description (self) :
		return "Entity"

	#default value None
	def get_controller (self) :
		return self.controller
	def set_controller (self, controller) :
		self.controller = controller

	#default value None
	def get_delegate (self) :
		return self.delegate
	def set_delegate (self, delegate) :
		self.delegate = delegate

	#does the entity collide with other entities?
	def is_physical (self) :
		return self.physical
	def set_physical (self, physical) :
		self.physical = physical

	#which direction is the entity facing?
	#irrelevant for some entities, but probably useful for most
	def get_direction (self) :
		return self.direction
	def set_direction (self, direction) :
		self.direction = direction

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

	#is this entity able to collide with the given entity?
	def can_collide_with_entity (self, entity) :
		return (entity is not self 
				and self.is_physical ()
				and entity.is_physical ()
				and not (entity in self.pass_through_entities) 
				and not (self in entity.pass_through_entities))

	#called when the entity is attacked by another entity
	#	can be refined in subclasses
	#	default implementation only looks at knockback
	def was_attacked (self, knockback, damage) :
		pass

	#can be overriden in subclasses
	#this code should be called anyway though
	def update (self) :
		if self.controller != None :
			self.controller.update (self)
		self.update_image ()

	#called after update
	#can be overridden. if the a subclass wishes to allow image scaling,
	#	it should call scale_image afterward
	def update_image (self) :
		key = self.images['default']
		self.image = resource.get_image (key)
		if self.direction == Direction.left :
			key += 'flip'
			if resource.has_image (key) :
				self.image = resource.get_image (key)
			else :
				self.image = pygame.transform.flip (self.image, True, False).convert ()
				resource.set_image (key, self.image)
		self.image.set_colorkey ((255,255,255))
		self.scale_image ()
	def scale_image (self) :
		if self.width != 0 or self.height != 0 :
			self.image = pygame.transform.scale (self.image, (self.width,self.height))


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