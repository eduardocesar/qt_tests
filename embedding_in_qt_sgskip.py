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


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QVBoxLayout(self._main)

        self.x = np.linspace(0, 10, 2000)
        self.y = np.sin(self.x)

        dynamic_canvas = self.create_figure(12, 3)

        dynamic_canvas1 = self.create_figure(12, 3)
        
        dynamic_canvas2 = self.create_figure(12, 3)

        # self.addToolBar(QtCore.Qt.BottomToolBarArea,
        #                 NavigationToolbar(dynamic_canvas, self))
        

        # self.addToolBar(NavigationToolbar(dynamic_canvas, self))

        # Plot 0 - Trying to optimize
        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._dynamic_ax.figure.canvas.draw()

        self.background = self._dynamic_ax.figure.canvas.copy_from_bbox(
            self._dynamic_ax.bbox)
        
        self.line, = self._dynamic_ax.plot(self.x, self.y, animated=True)

        # Start Timer 0
        self._timer = dynamic_canvas.new_timer(
            10, [(self._update_canvas, (), {})])
        self._timer.start()

        # Plot 1
        ax = dynamic_canvas1.figure.subplots()
        line, = ax.plot(self.x, self.y)
        ax.figure.canvas.draw() # Caches the render
        
        # timer 1
        self.timer = dynamic_canvas1.new_timer(
            10, [(self.update_canvas1, (line, ax), {})]
            )
        self.timer.start()
        
        # Plot and timer 2
        self.line2, self.ax2 = self.create_ax(dynamic_canvas2)
        self.timer2 = self.install_timer(self.line2, self.ax2, dynamic_canvas2)

    def _update_canvas(self):
        canvas = self._dynamic_ax.figure.canvas
        ax = self._dynamic_ax
        canvas.restore_region(self.background)
        
        # Shift the sinusoid as a function of time.
        u = np.sin(10*(self.x + time.time()))
        self.line.set_ydata(u)
        ax.draw_artist(self.line)
        canvas.blit(ax.bbox)
                
    def update_canvas1(self, line, ax):
        u = np.sin(10*(self.x + time.time()))
        line.set_ydata(u)
        ax.draw_artist(ax.patch)
        ax.draw_artist(line)
        ax.figure.canvas.update()
        ax.figure.canvas.flush_events()

    def create_figure(self, w, h):
        dynamic_canvas = FigureCanvas(Figure(figsize=(w, h)))
        self.layout.addWidget(dynamic_canvas)
        return dynamic_canvas

    def create_ax(self, canvas):
        ax = canvas.figure.subplots()
        line, = ax.plot(self.x, self.y)
        return line, ax

    def install_timer(self, line, ax, canvas):
        def update_canvas(line, ax):
            u = np.sin(10*(self.x + time.time()))
            line.set_ydata(u)
            ax.figure.canvas.draw()

        timer = canvas.new_timer(
            10, [(update_canvas, (line, ax), {})])
        timer.start()
        return timer
    

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
