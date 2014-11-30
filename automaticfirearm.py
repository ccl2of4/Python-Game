from firearm import Firearm

class AutomaticFirearm (Firearm) :
	def __init__(self, pos=(0,0), **images) :
		Firearm.__init__ (self,pos,**images)
		self._firing = False

	def get_description (self) :
		result = "Auto-Firearm ("
		if len (self._magazine) > 0 :
			result += self._magazine[0].get_description () + " x" + str (len (self._magazine))
		else :
			result += "Empty"
		result += ")"

		return result

	def begin_attacking (self) :
		self._firing = True
		Firearm.begin_attacking (self)

	#release the trigger
	def end_attacking (self) :
		self._firing = False
		Firearm.end_attacking (self)

	def _fire (self) :
		Firearm._fire (self)

	def update (self) : 
		assert (self._cooldown_frames_left >= 0)

		if self._cooldown_frames_left > 0 :
			self._cooldown_frames_left -= 1
		if self._firing and self._cooldown_frames_left == 0 :
			self._fire ()

		Firearm.update (self)