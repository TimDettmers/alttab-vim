import keyboard
import sys
from PyQt4 import QtGui, QtCore 
from winlaunch import *

# Press PAGE UP then PAGE DOWN to type "foobar".
def test(e):
    #print e.name
    pass

class KeyEvent:
    key = None

def uden():
    print 'kek'
    app = QtGui.QApplication(sys.argv)
    mywindow = mymainwindow()
    mywindow.show()
    mywindow2 = mymainwindow(1400)
    mywindow2.show()
    app.exec_()
    print KeyEvent.key




class mymainwindow(QtGui.QWidget):
    def __init__(self, offset=0):
        QtGui.QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
            )
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.offset = offset
        self.center()
        #QtCore.QTimer.singleShot(300, self.close)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        centerPoint = QtCore.QPoint(centerPoint.x()+self.offset, centerPoint.y())
        print(centerPoint)
        self.move(centerPoint)

    def mousePressEvent(self, event):
        QtGui.qApp.quit()

    def keyPressEvent(self, e):
        #if e.key() == QtCore.Qt.Key_Q:
        KeyEvent.key = e.key()
        QtGui.qApp.quit()




keyboard.add_hotkey('ctrl+alt+k', uden)
keyboard.hook(test)
keyboard.wait('esc')
