import matplotlib.pyplot as plt
import numpy as np
import math
import pickle


# Max distance to draw (in cm)
MAX_D = 500
STEP = 10

MIN_ANGLE_PAN = 0
MAX_ANGLE_PAN = 180
MIN_ANGLE_TILT = 80
MAX_ANGLE_TILT = 180
OFFSET_TILT = 80
PAN_INC = 5
TILT_INC = 1.25

def rot_x(angle):
    """ 3D rotation matrix about the x dir
    :param angle: int (degrees)
    :return: numpy array
    """
    angle = math.radians(angle)
    return np.array([[1, 0, 0],
                    [0, math.cos(angle), -math.sin(angle)],
                    [0, math.sin(angle), math.cos(angle)]])
def rot_y(angle):
    """ 3D rotation matrix about the y dir
    :param angle: int (degrees)
    :return: numpy array
    """
    angle = math.radians(angle)
    return np.array([[math.cos(angle), 0, math.sin(angle)],
                    [0, 1, 0],
                    [-math.sin(angle), 0, math.cos(angle)]])
def rot_z(angle):
    """ 3D rotation matrix about the z dir
    :param angle: int (degrees)
    :return: numpy array
    """
    angle = math.radians(angle)
    return np.array([[math.cos(angle), -math.sin(angle), 0],
                    [math.sin(angle), math.cos(angle), 0],
                    [0, 0, 1]])

def build(sweep):
    X = []
    Y = []
    Z = []
    # Quick and dirty method to build it from sweep
    for pan_angle in np.arange(MIN_ANGLE_PAN, MAX_ANGLE_PAN+PAN_INC, PAN_INC):
        for tilt_angle  in np.arange(MIN_ANGLE_TILT, MAX_ANGLE_TILT+TILT_INC, TILT_INC):
            row = (tilt_angle - MIN_ANGLE_TILT) / TILT_INC
            col = (pan_angle - MIN_ANGLE_PAN) / PAN_INC

            # Only get z for actual readings within the range we are looking at
            if sweep[row][col] < 0 or sweep[row][col] > MAX_D:
                continue
            else:
                distance = sweep[row][col]
                #print row, col, distance

            # intertial frame x-dir [left], y-dir [forward], z-dir [down]
            # Vec in {2}
            vec = np.array([0, distance, 0])
            # reverse the tilt {2} => {1}
            x2 = tilt_angle+90-OFFSET_TILT
            vec = np.dot(np.transpose(rot_x(x2)),vec)
            # reverse the pan {1} => {0}
            z1 = pan_angle-90
            vec = np.dot(np.transpose(rot_z(z1)),vec)

            #print vec

            # round the values to increments of STEP)
            X.append(int(round(vec[0])))
            Y.append(int(round(vec[1])))
            Z.append(int(round(vec[2])))

    return X,Y,Z

data_in = open('data.out')
data = pickle.load(data_in)



print "building z axis data"

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

frame = 1
for sweep in data:
    print frame
    x,y,z = build(sweep)
    # build plot and flip y and z
    ax.scatter(x, [i*-1 for i in y], [i*-1 for i in z], s=10)
    plt.pause(.0001)
    frame += 1

wait = input("PRESS ENTER TO CONTINUE.")
