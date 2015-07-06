from pubsub import pub 
from threading import Thread 
import time 
import random

class Lidar(Thread):

	def __init__(self):
		Thread.__init__(self)

	def run(self):
		print("Lidar thread started")
		for i in range(0,10):
			time.sleep(2)
			num = random.randint(0,100)
			print("Lidar thread: " + str(num))
			pub.sendMessage('newData',d=num)
