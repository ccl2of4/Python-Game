class LifeControllerClient :
	def life_controller_client_died (self) :
		pass

class LifeController :
	def __init__ (self) :
		self._max_health = 100
		self._health = 100
		self._client = None

	#the client whose life we are monitoring
	def get_client (self) :
		return self._client
	def set_client (self, client) :
		self._client = client

	#the maximum health that the client can have
	def get_max_health (self) :
		return self._max_health
	def set_max_health (self, max_health) :
		self._max_health = max_health

	#client's current health
	def get_health (self) :
		return self._health
	def set_health (self, health) :
		self._health = health

	#add logic to process input damage
	def receive_damage (self, damage) :
		self._health -= damage
		if self._health < 0:
			self._client.life_controller_client_died ()

	def kill (self) :
		self._receive_damage (self.health)