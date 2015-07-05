from pubsub import pub
from threading import Thread

class Command(Thread):

	def __init__(self):
		Thread.__init__(self)	

	def dataAdded(self, d):
		print("Command thread: " + str(d))

	def run(self):
		print("Command thread started")
		pub.subscribe(self.dataAdded, "newData")
