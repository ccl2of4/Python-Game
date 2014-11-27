from Bullet import Bullet
from Explosion import Explosion

class ExplosiveBullet (Bullet) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		Bullet.__init__ (self,x,y,width,height,**images)

	def made_contact (self, entity) :
		#spawn an explosion
		explosion = Explosion (self.rect.centerx, self.rect.centery, 40, 40)
		explosion.rect.center = self.rect.center
		for entity in self.friendly_entities :
			explosion.friendly_entities.append (entity)
		for entity in self.pass_through_entities :
			explosion.pass_through_entities.append (entity)
		self.delegate.spawn_entity (explosion)