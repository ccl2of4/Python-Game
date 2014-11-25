from Entity import *

class Direction :
	left = 0
	right = 1

class Projectile (Entity) :
	def __init__(self,x=0,y=0,width=0,height=0, **images) :
		Entity.__init__ (self,x,y,width,height,**images)

	def update (self) :
		Entity.update (self)

	def update_image (self) :
		Entity.update_image (self)

	def was_attacked (self) :
		pass

	def fire (self, velocity) :
		self.velocity = velocity