class NotificationCenter :

	_singleton = None

	def __init__ (self) :
		self._notifications = {}

	def add_observer (self, observer, notification_name) :
		if notification_name in self._notifications :
			observers = self._notifications[notification_name]
		else :
			observers = []
			self._notifications[notification_name] = observers
		observers.append (observer)
	def remove_observer (self, observer, notification_name) :
		if notification_name in self._notifications :
			observers = self._notifications[notification_name]
			observers.remove (observer)
	def post_notification (self, poster, notification_name, **info) :
		if notification_name in self._notifications :
			observers = self._notifications[notification_name]
			for observer in observers :
				observer.notify (poster, notification_name, **info)
	
	@classmethod
	def shared_center (cls) :
		if cls._singleton == None :
			cls._singleton = NotificationCenter ()
		return cls._singleton