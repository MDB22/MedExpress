import exceptions

from autopilot import *
from multiprocessing import Process

def main():
    ip = "tcp:127.0.0.1:5760"

    pixhawk = Autopilot(ip, None, None)

    # Activate the processes
    pixhawk.start()

    # About to exit script, make sure we cleanup
    # Block the calling thread until the process terminates,
    # or until the optional timeout occurs.
    pixhawk.join()

    print("Mission complete.")

if __name__ == '__main__':
    p = Process(target = main)
    p.start()
