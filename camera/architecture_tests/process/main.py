from processor import Processor

print "Start the main thread"

# start the other process
p = Processor()
q = Processor()


q.start()
p.start()



for i in range(0,50):
  print "this is the main thread ", i
  

p.stop()
