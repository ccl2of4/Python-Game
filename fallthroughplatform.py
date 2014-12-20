from entity import *

class FallThroughPlatform (Entity) :
	def __init__ (self, pos = (0,0), **images) :
		Entity.__init__ (self, pos, **images)
		self._needs_redraw = True

	def _additional_collision_conditions (self, entity) :
		return get_location (self.rect, entity.rect) == Location.below

	def update_image (self) :
		if self._needs_redraw :
			self.image = pygame.Surface ((200,10))
			self.image.fill ((100,100,100))
			self._needs_redraw = False