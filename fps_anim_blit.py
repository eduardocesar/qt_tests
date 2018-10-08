# -*- coding: utf-8 -*-

import sys
import time

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5

if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QVBoxLayout(self._main)

        self.tstart = None

        self.fps_label = QtWidgets.QLabel()

        self.fps_label.setText('FPS = {}'.format(0))

        self.layout.addWidget(self.fps_label)

        self.x = np.linspace(0, 10, 2000)
        self.y = np.sin(self.x)


        dynamic_canvas = FigureCanvas(Figure(figsize=(12, 3)))
        self.layout.addWidget(dynamic_canvas)

        # Plot 3 - Change animated and blit to True to superspeed!
        self.ax3 = dynamic_canvas.figure.subplots()
        self.line3,  = self.ax3.plot(self.x, self.y, animated=True)
        self.ani = FuncAnimation(dynamic_canvas.figure, self.animate, interval=0, blit=True)

    def animate(self, frame):
        if frame % 20 == 0:
            self.tstart = time.time()

        if frame % 20 == 10:
            fps = round(10/(time.time()-self.tstart), 2)
            self.fps_label.setText('FPS = {}'.format(fps))

            
        u = np.sin(10*(self.x + frame/10.0))
        self.line3.set_ydata(u)
        return [self.line3]

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
