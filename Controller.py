class Controller :

	def __init__ (self, entity=None) :
		self.entity = entity

	def get_entity (self) :
		return self.entity
	def set_entity (self, entity) :
		self.entity = entity

	def update (self) :
		pass