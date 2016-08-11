import atexit
import time
import signal
import curses

damn = curses.initscr()
damn.nodelay(1)

def handler(signum, frame):
  print 'c-Z pressed and ignored'



signal.signal(signal.SIGTSTP, handler)


while True:
  c = damn.getch()
  if c > 1:
    print "heelo" 
    break

