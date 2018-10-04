"""
===============
Embedding in Qt
===============

Simple Qt application embedding Matplotlib canvases.  This program will work
equally well using Qt4 and Qt5.  Either version of Qt can be selected (for
example) by setting the ``MPLBACKEND`` environment variable to "Qt4Agg" or
"Qt5Agg", or by first importing the desired version of PyQt.
"""

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
        layout = QtWidgets.QVBoxLayout(self._main)

        dynamic_canvas2 = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas2)
        self.addToolBar(NavigationToolbar(dynamic_canvas2, self))

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        self._dynamic_ax2 = dynamic_canvas2.figure.subplots()
        self._timer2 = dynamic_canvas2.new_timer(
            10, [(self._update_canvas2, (), {})])
        self._timer2.start()

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._timer = dynamic_canvas.new_timer(
            1, [(self._update_canvas, (), {})])
        self._timer.start()

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 1001)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(10*(t + time.time())))
        self._dynamic_ax.figure.canvas.draw()

    def _update_canvas2(self):
        self._dynamic_ax2.clear()
        t = np.linspace(0, 10, 1001)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax2.plot(t, np.sin(10*(t + time.time())))
        self._dynamic_ax2.figure.canvas.draw()
if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
