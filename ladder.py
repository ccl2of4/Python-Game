from entity import *

class Ladder (Entity) :
	def __init__ (self, pos = (0,0), **images) :
		Entity.__init__ (self, pos, **images)
		self.set_physical (False)

	def get_description (self) :
		return "Ladder"

	def interact (self, other) :
		v_x, v_y = other._velocity
		v_y = -other.get_gravity () - 10
		other._velocity = v_x, v_y