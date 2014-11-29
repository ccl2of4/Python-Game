import pygame
from entity import Entity

class EntitySpawnerDataSource :
	def entity_spawner_get_next_entity (self, enity_spawner) :
		pass
	def entity_spawner_get_cooldown (self, entity_spawner) :
		pass

class EntitySpawner (Entity) :
	def __init__ (self,x=0,y=0,width=100,height=100) :
		Entity.__init__(self,x,y,width,height)
		self.set_physical (False)

		self.entities = []
		self.cooldown = 120
		self.data_source = None
		self.frames_till_next_spawn = 0

	#the entities queued up to spawn
	def get_entities (self) :
		return self.entities
	def set_entities (self, entities) :
		self.entities = entities

	#how fast the entities spawn
	def get_cooldown (self) :
		return self.cooldown
	def set_cooldown (self, cooldown) :
		self.cooldown = cooldown

	#the above properties are ignored if data_source != None
	def get_delegate (self) :
		return self.data_source
	def set_delegate (self, delegate) :
		self.data_source = data_source

	def update (self) :

		if self.data_source == None :

			self.frames_till_next_spawn -= 1
			if (self.frames_till_next_spawn) < 0 and len (self.entities) > 0:
				entity = self.entities.pop(0)
				entity.rect.center = self.rect.center
				self.delegate.spawn_entity (entity)
				self.frames_till_next_spawn = self.get_cooldown ()
		else :
			pass

		Entity.update (self)

	def update_image (self) :
		self.image = pygame.Surface ((self.width, self.height))
		self.image.fill ((60,60,60))
		self.scale_image ()