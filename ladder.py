from entity import *

class Ladder (Entity) :
	def __init__ (self, pos = (0,0), **images) :
		Entity.__init__ (self, pos, **images)
		self._needs_redraw = True
		self.set_physical (False)

	def get_description (self) :
		return "Ladder"

	def interact (self, other) :
		v_x, v_y = other._velocity
		v_y = -other.get_gravity () - 10
		other._velocity = v_x, v_y

	def update_image (self) :
		if self._needs_redraw :
			self.image = pygame.Surface ( (50,500) )
			self.image.set_colorkey ((255,255,255))
			self.image.fill ((150,150,150))
			self._needs_redraw = False