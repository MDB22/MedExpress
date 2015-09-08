import multiprocessing
import time
import lidarSystem
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.art3d as art3d

#from itertools import combinations, product
from matplotlib.patches import Rectangle, PathPatch

class VoxelMap(multiprocessing.Process):
    
    def __init__(self, period, queue):
        # Call superclass init
        super(VoxelMap, self).__init__()
        
        self.period = period
        self.queue = queue
        
    def run(self):

    	# Attaching 3D axis to the figure
        fig = plt.figure()
        ax = p3.Axes3D(fig)

        # Fifty lines of random 3-D lines
        #data = [self.Gen_RandLine(25, 3) for index in range(50)]

        # Creating fifty line objects.
        # NOTE: Can't pass empty arrays into 3d version of plot()
        #lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

        # Setting the axes properties
        ax.set_xlim3d([0, 500])
        ax.set_xlabel('X')

        ax.set_ylim3d([-500, 500])
        ax.set_ylabel('Y')

        ax.set_zlim3d([-100, 500])
        ax.set_zlabel('Z')

        ax.set_title('3D Test')
        
        plt.show()
        
        # Timer for updating UAV parameters
        start = time.time()
        current = start
        
        while True:

            self.drawCube(ax, (100, 100, 100), (10, 10, 10))
            
            plt.canvas.blit(ax.bbox)
            
            return
            
            current = time.time()
            
            if (current - start > self.period):
                print "Printing Queue"
                # Get data from Queue
                data = self.queue.get()
                print data
                # Reset timer
                start = time.time()

        # Creating the Animation object
##        line_ani = animation.FuncAnimation(fig, self.update_lines, 25, fargs=(data, lines),
##                                      interval=50, blit=False)

    def drawCube(self, ax, center, dimensions):
        r = [100, 300]

##        # product get all length 3 combinations of the elements in r
##        # list converts to the list type
##        # np.array converts to numpy array
##        # combinations gets all pairs of elements in the array
##        for s, e in combinations(np.array(list(product(r,r,r))), 2):
##            if np.sum(np.abs(s-e)) == r[1]-r[0]:
##                ax.plot3D(*zip(s,e), color="b")

        x, y, z = center
        dx, dy, dz = dimensions
        
        print x, y, z
        print dx, dy, dz

        p = Rectangle((x - dx/2., y - dy/2.), dx, dy, alpha=0.8)
        ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, z=z - dz/2.,zdir="z")
        p = Rectangle((100, 100), 10, 10, alpha=0.8)
        ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, z=5,zdir="y")
        p = Rectangle((100, 100), 10, 10, alpha=0.8)
        ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, z=5,zdir="y")
        p = Rectangle((100, 100), 10, 10, alpha=0.8)
        ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, z=5,zdir="y")
        p = Rectangle((100, 100), 10, 10, alpha=0.8)
        ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, z=5,zdir="y")
        p = Rectangle((100, 100), 10, 10, alpha=0.8)
        ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, z=5,zdir="y")
        
    def Gen_RandLine(self, length, dims=2) :
        """
        Create a line using a random walk algorithm

        length is the number of points for the line.
        dims is the number of dimensions the line has.
        """
        lineData = np.empty((dims, length))
        lineData[:, 0] = np.random.rand(dims)
        for index in range(1, length) :
            # scaling the random numbers by 0.1 so
            # movement is small compared to position.
            # subtraction by 0.5 is to change the range to [-0.5, 0.5]
            # to allow a line to move backwards.
            step = ((np.random.rand(dims) - 0.5) * 0.1)
            lineData[:, index] = lineData[:, index-1] + step

        return lineData

    def update_lines(self, num, dataLines, lines) :
        for line, data in zip(lines, dataLines) :
            # NOTE: there is no .set_data() for 3 dim data...
            line.set_data(data[0:2, :num])
            line.set_3d_properties(data[2,:num])
        return lines



q = multiprocessing.Queue()

l = lidarSystem.LidarSystem(2, q)
v = VoxelMap(4, q)

#l.start()
v.start()

#l.join();
v.join();

del(l);
del(v);
