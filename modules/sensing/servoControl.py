# Uses the provided pipe to issue position commands to a given servo

import time

# Linear map from desired angle to control value
def linearMap(value, in_low, in_high, out_low, out_high):
        # Convert the initial value into a 0-1 range (float)
        value_scaled = (value - in_low) / float(in_high - in_low)

        # Convert the 0-1 range into a value in the new range.
        return out_low + value_scaled * (out_high - out_low)
        
class ServoControl:
    
    def __init__(self, id, name, limits, pipe):
        self.id = id
        self.name = name
        self.min_angle, self.max_angle, self.min_width, self.max_width = limits
        self.pipe = pipe
        
    def printLimits(self):
        print self.name + ' servo limits are:'
        print 'Min angle - ' + str(self.min_angle)
        print 'Max angle - ' + str(self.max_angle)
        print 'Min width - ' + str(self.min_width)
        print 'Max width - ' + str(self.max_width)
        
    # Sets the angle of the servo
    def setAngle(self, angle):
        
        pulseWidth = linearMap(angle, self.min_angle, self.max_angle, 
            self.min_width, self.max_width)
        
        self.setPosition(pulseWidth)
                
    # Sets the PWM output to the given pulse width for the servo
    def setPosition(self, width):
        # Throw exception if angle is not valid
        if (width < self.min_width or width > self.max_width):
            # IOError is the exception thrown by ServoBlaster
            raise IOError("Cannot set value " + str(width))
        
        self.pipe.write(str(self.id) + '=' + str(width) + 'us\n')
        self.pipe.flush()