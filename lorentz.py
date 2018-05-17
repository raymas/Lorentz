# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# created by raymas : lorentz script v0.1
#
######                ####### #     #
#     # ###### #####  #        #   #  ######
#     # #      #    # #         # #   #
######  #####  #    # #####      #    #####
#   #   #      #    # #          #    #
#    #  #      #    # #          #    #
#     # ###### #####  #######    #    ######
#
# Lorentz attractor for python using euler forward method : x(n+1) = x(n) + dt * f(x(t),t)
#
try :
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import matplotlib.pyplot as plt
except :
    print("matplotlib not present, checking PyQtGraph")

bIspyqtgraphPresent = True
try :
    from pyqtgraph.Qt import QtGui, QtCore
    import pyqtgraph as pg
    import pyqtgraph.opengl as gl
except :
    print("PyQtGraph is not present rollback to matplotlib...")
    bIspyqtgraphPresent = False

import time
import sys

# Euler paramters
delta = 0.01
path = []

# ---------------------------------------------------------------------------------------------

def lorentzAttractor(r, rho, beta, x, y, z) :
    """Lorentz Attractor using euler forward method"""
    global delta
    dx = x + delta * r * (y - x)
    dy = y + delta * (x * (rho - z) - y)
    dz = z + delta * (x * y - beta * z)
    return (dx, dy, dz)

# ---------------------------------------------------------------------------------------------

def liveLorentzAttractorMatplotlib(initialValues=[1,1,1], coef=[28, 10, 8/3], maxstep=300) :
    """Lorentz attractor plotted in real time !"""
    global path
    plt.ion()

    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.legend()

    lastValue = initialValues
    for i in range(0, maxstep) :
        lastValue = lorentzAttractor(20, 18, 8/3, lastValue[0], lastValue[1], lastValue[2])
        path.append(lastValue)
        pathnp = np.array(path)
        x, y, z = pathnp.T
        ax.plot(x, y, z, label='lorentz parametric curve')
        fig.canvas.draw()
        fig.canvas.flush_events()

# ---------------------------------------------------------------------------------------------

class LorentzVisualizer(object):
    def __init__(self, initialValues=[1,1,1], coef=[28, 10, 8/3], maxstep=1):
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 100
        self.w.setWindowTitle('Lorentz Attractor')
        #self.w.setGeometry(0, 110, 1920, 1080)
        self.w.show()

        self.initialValues = initialValues
        self.coef = coef
        self.maxstep = maxstep

        self.lastValue = initialValues
        self.path = []

        # create the background grids
        xgrid = gl.GLGridItem()
        xgrid.rotate(90, 0, 1, 0)
        xgrid.translate(-10, 0, 0)
        #xgrid.scale(0.1, 0.1, 0.1)
        self.w.addItem(xgrid)
        ygrid = gl.GLGridItem()
        ygrid.rotate(90, 1, 0, 0)
        ygrid.translate(0, -10, 0)
        #ygrid.scale(0.1, 0.1, 0.1)
        self.w.addItem(ygrid )
        zgrid = gl.GLGridItem()
        zgrid.translate(0, 0, -10)
        #zgrid.scale(0.1, 0.1, 0.1)
        self.w.addItem(zgrid)

        self.line = gl.GLLinePlotItem()
        self.w.addItem(self.line)

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def update(self):
        for i in range(self.maxstep) :
            self.lastValue = lorentzAttractor(20, 18, 8/3, self.lastValue[0], self.lastValue[1], self.lastValue[2])
            self.path.append(self.lastValue)
            self.line.setData(pos=np.array(self.path))

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(0.1)
        self.start()

# ---------------------------------------------------------------------------------------------


if __name__ == "__main__" :
    if bIspyqtgraphPresent :
        lorentzVisualizer = LorentzVisualizer(coef=[12, 10, 8/3]) # rho, r, beta
        lorentzVisualizer.animation()
    else :
        liveLorentzAttractorMatplotlib()
