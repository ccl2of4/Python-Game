class NotificationCenter :

	def __init__ (self) :
		self.notifications = {}

	def add_observer (self, observer, notification_name) :
		if notification_name in self.notifications :
			observers = self.notifications[notification_name]
		else :
			observers = []
			self.notifications[notification_name] = observers
		observers.append (observer)
	def remove_observer (self, observer, notification_name) :
		if notification_name in self.notifications :
			observers = self.notifications[notification_name]
			observers.remove (observer)
	def post_notification (self, poster, notification_name, **info) :
		if notification_name in self.notifications :
			observers = self.notifications[notification_name]
			for observer in observers :
				observer.notify (poster, notification_name, **info)

	singleton = None

NotificationCenter.singleton = NotificationCenter ()
def shared_center () :
	return NotificationCenter.singleton