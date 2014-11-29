from pygame import Rect

class Camera :
	def __init__(self, width=800, height=400):
		self.state = Rect(0, 0, width, height)
		self.target = None

	def get_target (self) :
		return self.target
	def set_target (self, target) :
		self.target = target

	def apply(self, entity):
		entity.rect.move_ip(self.state.topleft)

	def update(self):
		l, t, _, _ = self.target.rect # l = left,  t = top
		_, _, w, h = self.state      # w = width, h = height
		self.state = Rect(-l + w/2.0, -t + h/2.0, w, h)