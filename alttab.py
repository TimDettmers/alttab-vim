from __future__ import print_function
import keyboard
import sys
from PyQt4 import QtGui, QtCore
from winlaunch import *
from threading import Thread, Event
import time
import copy
from util import Timer
# Press PAGE UP then PAGE DOWN to type "foobar".

t = Timer()

class WindowPoller(Thread):
    def __init__(self):
        super(WindowPoller, self).__init__()
        daemon = True
        self.widget_params = []
        updating = False
        self.stop_updating = Event()


    def key_event_start(self):
        self.stop_updating.set()

    def key_event_stop(self):
        self.stop_updating.clear()

    def is_in_key_event(self):
        return self.stop_updating.isSet()


    def run(self):
        error = False
        i = 0
        t0 = time.time()
        while True:
            i+=1
            if i % 100 == 0:
                print(i, time.time() - t0)
            error = False
            try:
                wids = current_windows()
            except:
                print('ERROR')
                time.sleep(0.1)
                continue

            widgets = []
            key2wid = {}
            new_widget_params = []
            for i, wid in enumerate(wids):
                try:
                    if self.is_in_key_event(): break
                    pos, size, name = win_pos(wid), win_size(wid), win_name(wid)
                except:
                    print("ERROR")
                    error = True
                    break
                if 'alttab.py' == name: continue
                if pos is None: continue
                if 'unity' in name: continue
                if 'Desktop' in name: continue
                if pos[0] < 0 or pos[1] < 0: continue # todo: handle windows on other desktops
                if size is None: continue
                centerx = (pos[0]+size[0])-(size[0]/2)
                centery = (pos[1]+size[1])-(size[1]/2)
                p = [centerx, centery]
                new_widget_params.append([centerx, centery, keys[i], wid, scan_codes[i]])
            if error:
                time.sleep(0.1)
                continue
            self.widget_params = new_widget_params
            time.sleep(0.1)

class KeyEvent:
    key = None

keys = 'jfkdlshga;utreiwopmnvb'
scan_codes = [74, 70, 75, 68, 76, 83, 72, 71, 65, 59, 85, 84, 82, 69, 73, 87,79,80,77,78,86,66]

p = WindowPoller()
p.start()

def uden():
    t.tick('full')
    app = QtGui.QApplication(sys.argv)
    params = copy.deepcopy(p.widget_params)
    p.key_event_start()
    print(len(params))
    p.key_event_stop()
    if len(params) == 0: return
    widgets = []
    key2wid = {}
    t.tick('generate windows')
    for x, y, key, wid, scan_code in params:
        widgets.append(mymainwindow(x, y, key))
        key2wid[scan_code] = wid
        t.tick('show windows')
        widgets[-1].show()
        t.tick('show windows')
    t.tock('generate windows')
    t.tock('show windows')

    t.tick('exec app')
    app.exec_()
    t.tock('exec app')

    t.tick('focus')
    if KeyEvent.key in key2wid:
        focus(key2wid[KeyEvent.key])
    t.tock('focus')
    t.tock('full')
    p.key_event_stop()




class mymainwindow(QtGui.QLabel):
    def __init__(self, x, y, text):
        QtGui.QWidget.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint
            )
        #self.setLineWrapMode(QtGui.QTextEdit.FixedPixelWidth)
        self.setGeometry(x,y, 40,40)
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
