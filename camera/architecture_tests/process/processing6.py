from multiprocessing import Process, Pipe


def f(conn):
  for i in range(0,20):
    conn.send(42)
    
  conn.send(-1)
  conn.close()

def r(conn):
  while conn.recv() is not -1:
    print conn.recv()
  conn.close()
  print "closed"
  
parent_conn, child_conn = Pipe()

p = Process(target=f, args=(child_conn,))
q = Process(target=r, args=(parent_conn,))

p.start()
q.start()
p.join()
