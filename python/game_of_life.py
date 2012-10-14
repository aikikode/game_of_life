import sys
from PyQt4 import QtGui, QtCore
import time

__author__ = 'aikikode'

ROWS = 24
COLS = 20
STEP = 0.2

class PopulationWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.layMain = QtGui.QVBoxLayout()
        self.setWindowTitle("Life Game")
        self._generator = None
        self._timerId = None

        # add cells as buttons
        self.cell = [[Cell(x, y) for y in xrange(ROWS)] for x in xrange(COLS)]
        self.layMain = QtGui.QGridLayout(self)
        self.layMain.setHorizontalSpacing(0)
        self.layMain.setVerticalSpacing(0)
        [[self.layMain.addWidget(self.cell[x][y], x, y) for y in xrange(ROWS)] for x in xrange(COLS)]

        self.startButton = QtGui.QPushButton(self)
        self.startButton.setText("Start")
        self.startButton.setCheckable(True)
        self.layMain.addWidget(self.startButton, COLS / 2 - 1, ROWS)
        self.connect( self.startButton, QtCore.SIGNAL("clicked()"), self.startOrPause)

        self.nextStepButton = QtGui.QPushButton(self)
        self.nextStepButton.setText("Next Step")
        self.layMain.addWidget(self.nextStepButton, COLS / 2, ROWS)
        self.connect( self.nextStepButton, QtCore.SIGNAL("clicked()"), self.nextStep)

        self.clearButton = QtGui.QPushButton(self)
        self.clearButton.setText("Clear")
        self.layMain.addWidget(self.clearButton, COLS / 2 + 1, ROWS)
        self.connect( self.clearButton, QtCore.SIGNAL("clicked()"), self.clear)

        # Center Widget on screen
        screenWidth = QtGui.QDesktopWidget().screenGeometry(0).width()
        screenHeight = QtGui.QDesktopWidget().screenGeometry(0).height()
        size = self.sizeHint()
        self.move((screenWidth - size.width()) * 0.5, (screenHeight - size.height()) * 0.5)
    #def __init__(self)

    def startOrPause(self):
        if self.startButton.isChecked():
            self.startButton.setText("Pause")
            self.stop()                              # Stop any existing timer
            self._generator = self.startEvolution()  # Start the loop
            self._timerId = self.startTimer(0)       # This is the idle timer
        else:
            self.startButton.setText("Start")
            self.stop()

    def stop(self):
        if self._timerId is not None:
            self.killTimer(self._timerId)
        self._generator = None
        self._timerId = None

    def clear(self):
        [[self.cell[x][y].setChecked(False) for y in xrange(ROWS)] for x in xrange(COLS)]

    def nextStep(self):
        self.computeNewState()
        self.updatePopulation()
        if self.isGameFinished():
            self.startButton.setChecked(False)
            self.startOrPause()

    def timerEvent(self, event):
        # This is called every time the GUI is idle.
        if self._generator is None:
            return
        try:
            next(self._generator)
        except StopIteration:
            self.stop()  # kill the timer

    def startEvolution(self):
        while True:
            self.nextStep()
            time.sleep(STEP)
            yield

    def stopEvolution(self):
        self.stopTrigger = True

    def computeNewState(self):
        [[self.computeNewCellState(x ,y) for y in xrange(ROWS)] for x in xrange(COLS)]

    def computeNewCellState(self, x, y):
        relatives = self.analyse(x - 1, y - 1) + self.analyse(x - 1, y) + self.analyse(x - 1, y + 1) +\
                    self.analyse(x, y - 1) + self.analyse(x, y + 1) +\
                    self.analyse(x + 1, y - 1) + self.analyse(x + 1, y) + self.analyse(x + 1, y + 1)

        if 3 == relatives or (2 == relatives and self.cell[x][y].isAlive):
            self.cell[x][y].willBeAlive = True
        else:
            self.cell[x][y].willBeAlive = False

    def updatePopulation(self):
        [[self.updateCell(x, y) for y in xrange(ROWS)] for x in xrange(COLS)]

    def updateCell(self, x, y):
        self.cell[x][y].setChecked(self.cell[x][y].willBeAlive)

    def analyse(self, x, y):
        x %= COLS
        if x < 0:
            x += COLS
        y %= ROWS
        if y < 0:
            y += ROWS
        if self.cell[x][y].isAlive:
            return 1
        else:
            return 0

    def isGameFinished(self):
        for x in xrange(COLS):
            for y in xrange(ROWS):
                if self.cell[x][y].isAlive != self.cell[x][y].wasAlive:
                    return False
        return True
#class PopulationWidget(QtGui.QWidget)

class Cell(QtGui.QPushButton):
    def __init__(self, x, y):
        QtGui.QPushButton.__init__(self, str(x) + ":" + str(y))
        self.setMinimumHeight(30)
        self.setMaximumHeight(30)
        self.setMinimumWidth(30)
        self.setMaximumWidth(30)
        self.setCheckable(True)
        self.x = x
        self.y = y
        self.wasAlive = False
        self.isAlive = False
        self.willBeAlive = False
        self.setText("")

    def setChecked(self, bool):
        QtGui.QPushButton.setChecked(self, bool)
        self.wasAlive = self.isAlive
        self.setText("O" if bool else "")
        self.isAlive = bool

    def mousePressEvent(self, QMouseEvent):
        if self.isChecked():
            self.setChecked(False)
        else:
            self.setChecked(True)
#class Cell(QtGui.QPushButton)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mWidget = PopulationWidget()
    mWidget.show()
    sys.exit(app.exec_())
