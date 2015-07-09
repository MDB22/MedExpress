import smbus
import time

# Port assignment for Pi version 2
I2C_PORT = 1
    
# Register address for I2C port
I2C_REG = 0x62
    
# Register addresses for I2C data bytes
I2C_DATA_LOW = 0x10
I2C_DATA_HIGH = 0x0f

# Register addresses for setting measure mode
MEASURE_REG = 0x00
MEASURE_VAL = 0x04

# Frequency ranges for LiDAR
FREQ_MAX = 500
FREQ_MIN = 1

# Delay to allow LiDAR reads to settle, in seconds
SETTLING_DELAY = 1
    
class Lidar:
        
    def __init__(self, frequency):
        # Frequency is the update rate for reads from the LiDAR
        if (frequency < FREQ_MIN or FREQ_MAX < frequency):
            raise Exception
        
        self.delay = 1/float(frequency)
        
        # Communication bus to I2C
        self.bus = smbus.SMBus(I2C_PORT)
        
    def __del__(self):
        del(self.bus)
        
    def getRange(self):
        try:
            # Send measure byte
            result = self.bus.write_byte_data(I2C_REG, MEASURE_REG, MEASURE_VAL)
            
            # Wait for I2C communication
            time.sleep(self.delay)
            
            # Read from registers
            range_low = self.bus.read_byte_data(I2C_REG, I2C_DATA_LOW)
            range_high = self.bus.read_byte_data(I2C_REG, I2C_DATA_HIGH)
            range = (range_high << 8) + range_low
            
            return range
            
        except IOError:
            return -1
        
    def continuousRead(self):
        currentTime = time.time()
        
        # Dummy reads to allow data to settle
        while (time.time() - currentTime) < SETTLING_DELAY:
            self.getRange()
        
        # Read data continuously
        while True:
            range = self.getRange()
            print range
            
        return