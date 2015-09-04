import math
import numpy as np

angle = math.radians(45)

rot = np.array([[math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]])

m = np.transpose(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0]]))

result = np.dot(rot, m)

print "Initial matrix"
for row in m:
    for col in row:
        print "%3.2f" % col,
    
    print

print "Result matrix"
for row in result:
    for col in row:
        print "%3.2f" % col,
    
    print