from pubsub import pub
from threading import Thread

class Logger(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.data = []

	def dataAdded(self, d):
		self.data.append(d)
		print("Logger thread: " + str(self.data))

	def run(self):
		print("Logger thread started")
		pub.subscribe(self.dataAdded, 'newData')
