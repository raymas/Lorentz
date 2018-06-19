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
import numpy as np


engine_selection = "matplotlib" # or "pyqtgraph3D" or "pyqtgraph2D"

try :
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
except :
    print("matplotlib not present, checking PyQtGraph")

try :
    from pyqtgraph.Qt import QtGui, QtCore
    import pyqtgraph as pg
    import pyqtgraph.opengl as gl
except :
    print("PyQtGraph is not present")

import time
import sys
import threading

# Euler parameters
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

def liveLorentzAttractorMatplotlib(initialValues=[1,1,1], coef=[10, 28, 8/3], maxstep=10000) :
    """Lorentz attractor plotted in pseudo real time !"""
    global path

    plt.close('all')

    mpl.rcParams['legend.fontsize'] = 10
    fig3D = plt.figure(1)
    ax = fig3D.gca(projection='3d')
    ax.set_title("Lorentz System")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    #figAxis = plt.figure(2)
    figAxis, Axis = plt.subplots(3, sharex=True, sharey=True)
    [x.grid() for x in Axis]

    t = np.array([x for x in range(maxstep)])
    lastValue = initialValues
    for i in range(0, maxstep) :
        lastValue = lorentzAttractor(coef[0], coef[1], coef[2], lastValue[0], lastValue[1], lastValue[2])
        path.append(lastValue)
        pathnp = np.array(path)

    x, y, z = pathnp[:len(pathnp), 0], pathnp[:len(pathnp), 1], pathnp[:len(pathnp), 2]

    ax.set_xlim3d([x.min(), x.max()])
    ax.set_ylim3d([y.min(), y.max()])
    ax.set_zlim3d([z.min(), z.max()])

    line = ax.plot(x, y, z)
    lineX, = Axis[0].plot(t, x)
    lineY, = Axis[1].plot(t, y)
    lineZ, = Axis[2].plot(t, z)

    line_animation = animation.FuncAnimation(fig3D, update_lines, maxstep, fargs=(pathnp, line), interval=0.1, repeat=False, blit=False)
    #lines_animation = animation.FuncAnimation(figAxis, update_plots, maxstep, fargs=(pathnp, t, [lineX, lineY, lineZ]), interval=0.1, repeat=False, blit=False)

    plt.show();


def update_lines(num, dataLine, lines):
    for line in lines :
        line.set_data(dataLine[:num, 0], dataLine[:num, 1]) # x, y
        line.set_3d_properties(dataLine[:num, 2]) # z
    return lines

def update_plots(num, dataLine, timer, lines) :
    for i in range(len(lines)) :
        lines[i].set_xdata(timer[:num])
        lines[i].set_ydata(dataLine[:num, i])
    return lines

# ---------------------------------------------------------------------------------------------

class Lorentz3DVisualizer(object):
    def __init__(self, initialValues=[1,1,1], coef=[10, 28, 8/3], maxstep=1):
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 200
        self.w.setWindowTitle('Lorentz System')
        #self.w.setGeometry(0, 110, 1920, 1080)
        self.w.show()

        self.s = gl.GLGraphicsItem.GLGraphicsItem()
        self.s.show()

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

        self.first = time.time()

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def update(self):
        if time.time() - self.first < 2  :
            return

        for i in range(self.maxstep) :
            self.lastValue = lorentzAttractor(self.coef[0], self.coef[1], self.coef[2], self.lastValue[0], self.lastValue[1], self.lastValue[2])
            self.path.append(self.lastValue)
            self.line.setData(pos=np.array(self.path))

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(0.1)
        self.start()

# ---------------------------------------------------------------------------------------------

class Lorentz2DVisualizer(object):
    def __init__(self, initialValues=[1,1,1], coef=[10, 28, 8/3], maxstep=1):
        self.app = QtGui.QApplication(sys.argv)
        self.w = pg.GraphicsWindow(title="2D Lorentz system")
        self.w.resize(1000,600)

        self.pX = self.w.addPlot(title="X")
        self.curveX = self.pX.plot(pen='r')
        self.pX.showGrid(x=True, y=True)
        self.w.nextRow()

        self.pY = self.w.addPlot(title="Y")
        self.curveY = self.pY.plot(pen='g')
        self.pY.showGrid(x=True, y=True)
        self.w.nextRow()

        self.pZ = self.w.addPlot(title="Z")
        self.curveZ = self.pZ.plot(pen='b')
        self.pZ.showGrid(x=True, y=True)

        self.maxstep = maxstep
        self.lastValues = initialValues
        self.path = []
        self.coef = coef

        self.counter = 0

        self.first = time.time()

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def update(self):
        if time.time() - self.first < 0  :
            return
        for i in range(self.maxstep) :
            self.lastValues = lorentzAttractor(self.coef[0], self.coef[1], self.coef[2], self.lastValues[0], self.lastValues[1], self.lastValues[2])
            self.path.append(self.lastValues)
            pathnp = np.array(self.path)
            self.curveX.setData(np.array(pathnp[:len(pathnp), 0]))
            self.curveY.setData(np.array(pathnp[:len(pathnp), 1]))
            self.curveZ.setData(np.array(pathnp[:len(pathnp), 2]))


    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(0.1)
        self.start()

# ---------------------------------------------------------------------------------------------

if __name__ == "__main__" :
    if engine_selection == "pyqtgraph2D" :
        lorentzVisualizer = Lorentz2DVisualizer(coef=[10, 50, 8/3])
        lorentzVisualizer.animation()
    elif engine_selection == "matplotlib" :
        liveLorentzAttractorMatplotlib()
    elif engine_selection == "pyqtgraph3D" :
        lorentzVisualizer = Lorentz3DVisualizer(coef=[10, 50, 8/3])
        lorentzVisualizer.animation()
