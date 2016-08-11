from multiprocessing import Process

class Processor:
  def __init__(self):
    print "-- processor init --"
    self.p = Process(target=self.update(), args=())

  def update(self):
    for i in range(0,100):
      print "update! ", i
    print "updator finished"

  def start(self):
    print "processor started"
    self.p.start()

  def stop(self):
    print "processor ended"
    self.p.terminate()
