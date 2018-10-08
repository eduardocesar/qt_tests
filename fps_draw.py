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

        self.tstart = 0
        self.counter = 0
        
        self.fps_label = QtWidgets.QLabel()

        self.fps_label.setText('FPS = {}'.format(0))

        self.layout.addWidget(self.fps_label)

        self.x = np.linspace(0, 10, 2000)
        self.y = np.sin(self.x)


        dynamic_canvas1 = self.create_figure(12, 3)

        # Plot 1
        ax = dynamic_canvas1.figure.subplots()
        line, = ax.plot(self.x, self.y)
        
        #timer 1
        self.timer = dynamic_canvas1.new_timer(
            1, [(self.update_canvas1, (line, ax), {})]
            )
        self.timer.start()
        



    def update_canvas1(self, line, ax):
        self.counter += 1
        if self.counter % 20 == 0:
            self.tstart = time.time()

        if self.counter % 20 == 10:
            fps = round(10/(time.time()-self.tstart), 2)
            self.fps_label.setText('FPS = {}'.format(fps))


        u = np.sin(10*(self.x + time.time()))
        line.set_ydata(u)
        ax.figure.canvas.draw()

    def create_figure(self, w, h):
        dynamic_canvas = FigureCanvas(Figure(figsize=(w, h)))
        self.layout.addWidget(dynamic_canvas)
        return dynamic_canvas

    

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
