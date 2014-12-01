import pygame
from entity import Entity

class EntitySpawnerDataSource :
	def entity_spawner_get_next_entity (self, enity_spawner) :
		pass
	def entity_spawner_get_cooldown (self, entity_spawner) :
		pass

class EntitySpawner (Entity) :
	def __init__ (self,pos = (0,0),height=100, size = (200,200)) :
		Entity.__init__(self,pos)
		self.set_physical (False)

		self._layer = -1
		self._size = size
		self._entities = []
		self._cooldown = 600
		self._data_source = None
		self._frames_till_next_spawn = 0
		self._should_update_image = True

	#the entities queued up to spawn
	def get_entities (self) :
		return self._entities
	def set_entities (self, entities) :
		self._entities = entities

	#how fast the entities spawn
	def get_cooldown (self) :
		return self._cooldown
	def set_cooldown (self, cooldown) :
		self._cooldown = cooldown

	#the above properties are ignored if data_source != None
	def get_data_source (self) :
		return self._data_source
	def set_data_source (self, delegate) :
		self._data_source = data_source

	def update (self) :

		if self._data_source == None :

			self._frames_till_next_spawn -= 1
			if (self._frames_till_next_spawn) < 0 and len (self._entities) > 0:
				entity = self._entities.pop(0)
				entity.rect.center = self.rect.center
				self._delegate.spawn_entity (entity)
				self._frames_till_next_spawn = self.get_cooldown ()
		else :
			pass

		Entity.update (self)

	def update_image (self) :
		if self._should_update_image :
			self.image = pygame.Surface (self._size)
			self.image.fill ((60,60,60))
			self._should_update_image = False
		assert (self.image != None)