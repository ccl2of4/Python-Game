import pygame
import constants

class EntityDelegate :
	def get_all_entities () :
		pass

class Location :
	above = 2 << 1
	below = 2 << 2
	left = 2 << 3
	right = 2 << 4
	none = 2 << 5

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
		self.delegate = None
		self.image = None
		self.update_image ()
		self.rect = self.image.get_rect ()
		self.rect.move_ip (x,y)


	def get_delegate (self) :
		return self.delegate
	def set_delegate (self, delegate) :
		self.delegate = delegate

	def is_physical (self) :
		return self.physical
	def set_physical (self, physical) :
		self.physical = physical

	def is_affected_by_gravity (self) :
		return self.affected_by_gravity
	def set_affected_by_gravity (self, affected_by_gravity) :
		self.affected_by_gravity = affected_by_gravity

	def update (self) :

		v_x = self.velocity[0]
		v_y = self.velocity[1]
		self.grounded = False

		entities = self.delegate.get_all_entities ()

		if self.affected_by_gravity :
			v_y += constants.gravity
			for entity in entities :
				if entity is self :
					continue
					
				location = self.location (entity)
				if Location.below == location :
					v_y = max (v_y, entity.rect.top - self.rect.bottom)
				elif Location.above == location :
					v_y = min (v_y, entity.rect.top - self.rect.bottom)

				elif Location.left == location :
					v_x = min (v_x, entity.rect.left - self.rect.right)
				elif Location.right == location :
					v_x = max (v_x, entity.rect.right - self.rect.left)

				touching = self.touching (entity)
				if (Location.above == touching) :
					self.grounded = True

		if self.grounded :
			pass

		self.velocity = v_x, v_y
		self.rect.move_ip (*self.velocity)
		self.update_image ()

	def update_image (self) :
		if self.image == None :
			self.image = pygame.image.load (self.images['default'])
		if self.width != 0 or self.height != 0 :
			self.image = pygame.transform.scale (self.image, (self.width,self.height))

	def location (self, other) :
		if (self.rect.right <= other.rect.left and self.rect.bottom > other.rect.top and self.rect.top < other.rect.bottom) :
			return Location.left
		if (self.rect.left >= other.rect.right and self.rect.bottom > other.rect.top and self.rect.top < other.rect.bottom) :
			return Location.right
		if (self.rect.top >= other.rect.bottom and self.rect.right > other.rect.left and self.rect.left < other.rect.right) :
			return Location.below
		if (self.rect.bottom <= other.rect.top and self.rect.right > other.rect.left and self.rect.left < other.rect.right) :
			return Location.above
		else :
			return Location.none

	def touching (self, other) :
		if (self.rect.right == other.rect.left and (self.rect.bottom <= other.rect.top and self.rect.top >= other.rect.bottom)) :
			return Location.right
		if (self.rect.left == other.rect.right and (self.rect.bottom <= other.rect.top and self.rect.top >= other.rect.bottom)) :
			return Location.left
		if (self.rect.top == other.rect.bottom and (self.rect.right >= other.rect.left and self.rect.left <= other.rect.right)) :
			return Location.below
		if (self.rect.bottom == other.rect.top and (self.rect.right >= other.rect.left and self.rect.left <= other.rect.right)) :
			return Location.above
		else :
			return Location.none
