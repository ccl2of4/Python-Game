from entity import *

class Door (Entity) :
	def __init__ (self, pos = (0,0), **images) :
		Entity.__init__ (self, pos, **images)
		self._closed = True
		self._total_cooldown_frames = 30
		self._cooldown_frames_left = 0

	def get_description (self) :
		return "Door"

	def interact (self, other) :
		if self._cooldown_frames_left == 0 :
			self._closed = not self._closed
			self._cooldown_frames_left = self._total_cooldown_frames

	def _additional_collision_conditions (self, entity) :
		return self._closed

	def update (self) :
		if self._cooldown_frames_left > 0 :
			self._cooldown_frames_left -= 1
		Entity.update (self)

	def update_image (self) :

		direction = self._direction

		key = None

		if self._closed :
			key = self._images['closed']
		else :
			key = self._images['open']

		self.image = resource.get_image (key)
		if self._direction == Direction.left :
			key += 'flip'
			if resource.has_image (key) :
				self.image = resource.get_image (key)
			else :
				self.image = pygame.transform.flip (self.image, True, False).convert()
				resource.set_image (key, self.image)

		self.image.set_colorkey ((255,255,255))