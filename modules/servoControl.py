# Uses the provided pipe to issue position commands to a given servo

import time
        
class ServoControl:
    
    def __init__(self, id):
        self.id = id
        
    # Sets the PWM output to the given pulse width for the servo
    def setPosition(self, pipe, width):
        pipe.write(str(self.id) + '=' + str(width) + 'us\n')
        pipe.flush()