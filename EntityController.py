#base class for a controller for an entity
class EntityController :

	def __init__ (self, entity=None) :
		self.entity = entity

	def get_entity (self) :
		return self.entity
	def set_entity (self, entity) :
		self.entity = entity

	#overriden by subclasses
	#do logic here to control an entity
	def update (self) :
		pass