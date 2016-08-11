from multiprocessing import Process

def f(name):
  print "Hello, ", name


p = Process(target=f, args=('bob',))
p.start()
for i in range(0,100):
  print "ASDASLKDM"
p.join()
