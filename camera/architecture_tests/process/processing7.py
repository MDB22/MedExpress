from multiprocessing import Process, Lock

def f(l, i):
  l.acquire()
  print 'hello world', i
  l.release()

lock = Lock()

for num in range(10):
  Process(target=f, args=(lock, num)).start()
