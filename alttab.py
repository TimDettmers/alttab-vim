import keyboard
import sys
from PyQt4 import QtGui, QtCore
from winlaunch import *

# Press PAGE UP then PAGE DOWN to type "foobar".

class KeyEvent:
    key = None

keys = 'jfkdlshga;ut'
scan_codes = [74, 70, 75, 68, 76, 83, 72, 71, 65, 59, 85, 84]

def uden():
    app = QtGui.QApplication(sys.argv)
    wids = current_windows()
    widgets = []
    key2wid = {}
    wid2data = {}
    for i, wid in enumerate(wids):
        pos, size, name = win_pos(wid), win_size(wid), win_name(wid)
        if pos is None: continue
        if 'unity' in name: continue
        if 'Desktop' in name: continue
        centerx = (pos[0]+size[0])-(size[0]/2)
        centery = (pos[1]+size[1])-(size[1]/2)
        p = [centerx, centery]
        widgets.append(mymainwindow(centerx, centery, keys[i]))
        key2wid[scan_codes[i]] = wid
        widgets[-1].show()
        wid2data[wid] = [name, pos, size]
        print [wid, name]
    app.exec_()
    print KeyEvent.key

    focus(key2wid[KeyEvent.key])




class mymainwindow(QtGui.QLabel):
    def __init__(self, x, y, text):
        QtGui.QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint
            )
        #self.setLineWrapMode(QtGui.QTextEdit.FixedPixelWidth)
        self.move(x,y)
        self.resize(40,40)
        font = self.font()
        font.setFamily("Courier")
        font.setPointSize(20)
        fgcolor = QtGui.QColor('#474640')
        bgcolor = QtGui.QColor('#3AD7AF')
        P = self.palette()
        P.setColor(QtGui.QPalette.Background, bgcolor)
        P.setColor(QtGui.QPalette.Foreground, fgcolor)
        self.setPalette(P)

        self.setFont(font)
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignCenter)


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
keyboard.wait()
