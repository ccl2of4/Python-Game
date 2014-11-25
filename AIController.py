from Controller import Controller

class AIController (Controller) :
	def __init__ (self, entity) :
		Controller.__init__ (self, entity)
		self.target_entity = None

	def get_target_entity (self) :
		return self.target_entity
	def set_target_entity (self, target_entity) :
		self.target_entity = target_entity

	def update (self) :
		if self.target_entity.rect.center > self.entity.rect.center :
			self.entity.look_right ()
		else :
			self.entity.look_left ()

		self.entity.walk (False)

		if self.target_entity.rect.center < self.entity.rect.center :
			self.entity.jump ()