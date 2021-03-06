from pygame import Rect

class Camera :
	def __init__(self, width=800, height=400):
		self._state = Rect(0, 0, width, height)
		self._target = None

	def get_target (self) :
		return self._target
	def set_target (self, target) :
		self._target = target

	def set_state (self, state) :
		self._state = state
	def get_state (self) :
		return self._state

	def apply(self, entity):
		entity.rect.move_ip(self._state.topleft)

	def update(self):
		l, t, _, _ = self._target.rect # l = left,  t = top
		_, _, w, h = self._state      # w = width, h = height
		self._state = Rect(1.0*w/4.0 - l,h/2.0 - t, w, h)