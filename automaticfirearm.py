from firearm import Firearm

class AutomaticFirearm (Firearm) :
	def __init__(self,x=0,y=0,width=50,height=5, **images) :
		Firearm.__init__ (self,x,y,width,height,**images)
		self.firing = False

	def get_description (self) :
		result = "Auto-Firearm ("
		if len (self.magazine) > 0 :
			result += self.magazine[0].get_description () + " x" + str (len (self.magazine))
		else :
			result += "Empty"
		result += ")"

		return result

	def begin_attacking (self) :
		self.firing = True
		Firearm.begin_attacking (self)

	#release the trigger
	def end_attacking (self) :
		self.firing = False
		Firearm.end_attacking (self)

	def fire (self) :
		Firearm.fire (self)

	def update (self) : 
		assert (self.cooldown_frames_left >= 0)

		if self.cooldown_frames_left > 0 :
			self.cooldown_frames_left -= 1
		if self.firing and self.cooldown_frames_left == 0 :
			self.fire ()

		Firearm.update (self)