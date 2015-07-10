from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import time

def generate(X, Y, phi):
    R = 1 - np.sqrt(X**2 + Y**2)
    return np.cos(2 * np.pi * X + phi) * R

surf_args = {'rstride':1,
            'cstride':1,
            'cmap':cm.gray,
            'linewidth':0,
            'antialiased':False}

wframe_args = {'rstride':1,
            'cstride':1}
SIZE=2
STEP=0.1

xs = np.arange(-SIZE/2, SIZE/2, STEP)
ys = np.arange(-SIZE/2, SIZE/2, STEP)
X, Y = np.meshgrid(xs, ys)
Z = generate(X, Y, 0.0)


fig = plt.figure()
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')


wframe = None
surf = None
tstart = time.time()
for phi in np.linspace(0, 360 / 2 / np.pi, 100):

    wframe_old = wframe
    surf_old = surf

    Z = generate(X, Y, phi)
    #ax = fig.add_subplot(121, projection='3d')
    wframe = ax1.plot_wireframe(X, Y, Z, **wframe_args)
    surf = ax2.plot_surface(X, Y, Z, **surf_args)

    # Remove old line collection before drawing
    if wframe_old is not None:
        ax1.collections.remove(wframe_old)
        ax2.collections.remove(surf_old)

    plt.pause(.001) #Otherwise too fast

print ('FPS: %f' % (100 / (time.time() - tstart)))
