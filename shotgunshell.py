from projectile import Projectile
from bullet import Bullet

class ShotgunShell (Projectile) :
	def __init__ (self,x=0,y=0,width=10,height=10, **images) :
		Projectile.__init__ (self,x,y,width,height,**images)
		self.spread = .10

	def get_description (self) :
		return "Shotgun Shell"

	def launch (self, velocity) :
		
		b1 = Bullet (default='images/platform.png')
		b1.rect.x = self.rect.x
		b1.rect.y = self.rect.y

		b2 = Bullet (default='images/platform.png')
		b2.rect.x = self.rect.x
		b2.rect.y = self.rect.y

		b3 = Bullet (default='images/platform.png')
		b3.rect.x = self.rect.x
		b3.rect.y = self.rect.y

		entities_list  = self.get_pass_through_entities ()
		entities_list.extend ([self, b1, b2, b3])

		b1.set_pass_through_entities (entities_list)
		b1.set_friendly_entities (entities_list)
		
		b2.set_pass_through_entities (entities_list)
		b2.set_friendly_entities (entities_list)

		b3.set_pass_through_entities (entities_list)
		b3.set_friendly_entities (entities_list)

		self.delegate.spawn_entity (b1)
		b1.launch ( (velocity[0], -1) )

		self.delegate.spawn_entity (b2)
		b2.launch ( (velocity[0], 0) )

		self.delegate.spawn_entity (b3)
		b3.launch ( (velocity[0], 1) )

		self.delegate.despawn_entity (self)

	def get_spread (self) :
		return self.spread
	def set_spread (self, spread) :
		self.spread = spread

	def made_contact (self, entity) :
		assert (False)

	def update (self) :
		Projectile.update (self)

	def calculate_knockback (self, entity) :
		return (0,0)