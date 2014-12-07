from bullet import Bullet
from explosion import Explosion

class ExplosiveBullet (Bullet) :
	def __init__(self,x=0,y=0,width=5,height=5, **images) :
		Bullet.__init__ (self,x,y,width,height,**images)
		self._name = "Explosive Bullet"

	def made_contact (self, entity) :
		#spawn an explosion
		explosion = Explosion (self.rect.centerx, self.rect.centery, 40, 40)
		explosion.rect.center = self.rect.center
		for entity in self._friendly_entities :
			explosion._friendly_entities.append (entity)
		for entity in self._pass_through_entities :
			explosion._pass_through_entities.append (entity)
		self._delegate.spawn_entity (explosion)