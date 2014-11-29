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
	def __init__(self, x=0, y=0, width=120, height=50) :
		self.client = None
		Entity.__init__ (self,x,y,width,height)
		self.set_physical (False)
		self.set_gravity (0)

	def get_client (self) :
		return self.client
	def set_client (self, client) :
		self.client = client

	def update (self) :
		Entity.update (self)

	def update_image (self) :
		self.image = pygame.Surface ((self.width, self.height))
		self.image.set_colorkey ((255,255,255))
		self.image.fill ((255,255,255))

		if self.client != None :
			self.add_health_bar ()
			self.add_name ()
			self.add_weapon ()

		self.scale_image ()

	def add_health_bar (self) :
		#max health
		health_bar_rect = self.image.get_rect ()
		health_bar_rect.height *= .3
		health_bar_rect.bottom = self.image.get_rect().bottom
		pygame.draw.rect (self.image, (0,0,0), health_bar_rect, 1)

		#current health
		health_percent = 1.0 * self.client.get_health () / self.client.get_max_health ()
		cur_health_bar_rect = health_bar_rect
		cur_health_bar_rect.width *= health_percent
		pygame.draw.rect (self.image, (255,0,0), health_bar_rect)


	def add_name (self) :
		font = pygame.font.Font (None, 20)
		text = font.render (self.client.get_name (), 1, (0,0,0))
		textpos = text.get_rect ()
		textpos.centerx = self.image.get_rect().centerx
		textpos.top = self.image.get_rect().top
		self.image.blit (text, textpos)

	def add_weapon (self) :
		font = pygame.font.Font (None, 20)
		text = font.render (self.client.get_weapon_str (), 1, (0,0,0))
		textpos = text.get_rect ()
		textpos.centerx = self.image.get_rect().centerx
		textpos.centery = self.image.get_rect().centery
		self.image.blit (text, textpos)