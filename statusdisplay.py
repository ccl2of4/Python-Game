from entity import *

class StatusDisplayClient :
	def get_health (self) :
		pass
	def get_max_health (self) :
		pass
	def get_name (self) :
		pass
	def get_weapon_str (self) :
		pass

class StatusDisplay (Entity) :
	def __init__(self, pos = (0,0), size = (100,50)) :
		Entity.__init__ (self,pos)
		self._client = None
		self.set_physical (False)
		self._layer = 10
		self._size = size

		#for performance
		self._needs_redraw = True

		self._health = None
		self._max_health = None
		self._name = None
		self._weapon_str = None

	def get_client (self) :
		return self._client
	def set_client (self, client) :
		self._client = client

	def update (self) :
		assert (self._client != None)

		old_health = self._health
		old_max_health = self._max_health
		old_name = self._name
		old_weapon_str = self._weapon_str

		self._health = self._client.get_health ()
		self._max_health = self._client.get_max_health ()
		self._name = self._client.get_name ()
		self._weapon_str = self._client.get_weapon_str ()

		self._needs_redraw = (
			self._health != old_health or
			self._max_health != old_max_health or
			self._name != old_name or
			self._weapon_str != old_weapon_str)

		Entity.update (self)


	def update_image (self) :
		if self._needs_redraw :
			if self.image == None :
				self.image = pygame.Surface (self._size)
				self.image.set_colorkey ((255,255,255))

			self.image.fill ((255,255,255))
			self._add_health_bar ()
			self._add_name ()
			self._add_weapon ()

	def _add_health_bar (self) :
		#max health
		health_bar_rect = self.image.get_rect ()
		health_bar_rect.height *= .3
		health_bar_rect.bottom = self.image.get_rect().bottom
		pygame.draw.rect (self.image, (0,0,0), health_bar_rect, 1)

		#current health
		health_percent = 1.0 * self._health / self._max_health
		cur_health_bar_rect = health_bar_rect
		cur_health_bar_rect.width *= health_percent
		pygame.draw.rect (self.image, (255,0,0), health_bar_rect)


	def _add_name (self) :
		font = pygame.font.Font (None, 20)
		text = font.render (self._name, False, (100,100,100), (255,255,255)).convert ()
		textpos = text.get_rect ()
		textpos.centerx = self.image.get_rect().centerx
		textpos.top = self.image.get_rect().top
		self.image.blit (text, textpos)

	def _add_weapon (self) :
		font = pygame.font.Font (None, 20)
		text = font.render (self._weapon_str, False, (100,100,100), (255,255,255)).convert ()
		textpos = text.get_rect ()
		textpos.centerx = self.image.get_rect().centerx
		textpos.centery = self.image.get_rect().centery
		self.image.blit (text, textpos)