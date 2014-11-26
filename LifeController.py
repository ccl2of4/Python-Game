class LifeControllerClient :
	def life_controller_client_died (self) :
		pass

class LifeController :
	def __init__ (self) :
		self.max_health = 100
		self.health = 100
		self.client = None

	def get_client (self) :
		return self.client
	def set_client (self, client) :
		self.client = client

	#the maximum health that the client can have
	def get_max_health (self) :
		return self.max_health
	def set_max_health (self, max_health) :
		self.max_health = max_health

	#client's current health
	def get_health (self) :
		return self.health
	def set_health (self, health) :
		self.health = health

	#add logic to process input damage
	def receive_damage (self, damage) :
		self.health -= damage
		if self.health < 0:
			self.client.life_controller_client_died ()