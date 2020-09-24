from __future__ import print_function
import keyboard
import sys
from winlaunch import *
from threading import Thread, Event
import time
import copy
from util import Timer
import itertools
import tkinter as tk
import tkinter.font as font


t = Timer()

num_multi_keys = 1
keys = [key for key in 'jkfdlshga;utreiwopqmnbvcxz']
scan_codes = [74, 75, 70, 68, 76, 83, 72, 71, 65, 59, 85, 84, 82, 69, 73, 87,79,80, 81, 77, 78, 66, 86, 67, 88, 90]
main_keys = keys[:num_multi_keys]
secondary_keys = keys[num_multi_keys:]
main_codes = scan_codes[:num_multi_keys]
secondary_codes = scan_codes[num_multi_keys:]
multi_keys = [r for r in itertools.product(main_keys, secondary_keys)]
multi_codes = [r for r in itertools.product(main_codes, secondary_codes)]
keys = keys[num_multi_keys:] #+ multi_keys
scan_codes = scan_codes[num_multi_keys:] #+ multi_codes


polling_interval = 2.0

class KeyDisplay:
    def __init__(self, master, text):
        self.master = master
        self.text = tk.StringVar()
        self.text.set(text)
        self.frame = tk.Frame(self.master, width=40, height=40)
        self.lbl = tk.Label(self.frame, textvariable=self.text, bg='#3AD7AF', fg='#474640', height=1, width=10)
        self.lbl['font'] = font.Font(size=15)
        self.lbl.pack()
        self.frame.pack()
        self.master.overrideredirect(1)
        self.master.geometry('+0+0')
        self.master.withdraw()

    def close_windows(self):
        self.master.destroy()



class WindowManager:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, width=40, height=40)
        self.button1 = tk.Button(self.frame, text = 'Close', width = 5, command = self.close)
        self.button1.pack()

        self.master.bind("<KeyPress>", self.select_via_key)

        self.frame.pack()
        self.windows = []
        self.key2window = {}
        self.event = False
        for mkeys in keys:
            text = ''.join(mkeys)
            newWindow = tk.Toplevel(self.master)

            window = KeyDisplay(newWindow, text)
            self.key2window[mkeys] = window

        self.moved_windows = []
        self.key2wid = {}

    def move(self, key, x, y, name):
        window = self.key2window[key]
        chunks = name.split(' ')[::-1]
        app_text = ''
        while len(app_text) < 10:
            chunk = chunks.pop(0)
            if chunk == '-': continue
            if chunk == '|': continue
            if len(chunk) + len(app_text) > 10: break
            app_text = chunk + app_text


        window.text.set('{0} {1}'.format(key, app_text))
        window.master.geometry('+{0}+{1}'.format(int(x), int(y)))
        window.master.deiconify()
        #window.master.update()
        self.moved_windows.append(window)


    def reset(self):
        for window in self.moved_windows:
            #window.master.geometry('+0+0')
            window.master.withdraw()
        self.moved_windows = []
        self.event = False

    def close(self):
        self.master.destroy()

    def select_via_key(self, event):
        if self.event:
            if event.char in self.key2wid:
                focus(self.key2wid[event.char])
                self.reset()





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
                print('Processed {0} polls in {1} seconds ({2} seconds of waiting)'.format(i, time.time() - t0, 0.1*i))
            error = False
            try:
                wids = current_windows()
            except:
                print('ERROR')
                time.sleep(polling_interval)
                continue

            widgets = []
            key2wid = {}
            new_widget_params = []
            for j, wid in enumerate(wids):
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
                if 'tk' in name: continue
                if 'launcher' in name: continue
                if 'Desktop' in name: continue
                pos = list(pos)
                size = list(size)
                if pos[0] < 0 or pos[1] < 0: continue # todo: handle windows on other desktops
                if size is None: continue
                centerx = (pos[0]+size[0])-(size[0]/2)
                centery = (pos[1]+size[1])-(size[1]/2)
                p = [centerx, centery]
                new_widget_params.append([centerx, centery, keys[j], wid, scan_codes[j], name])
            if error:
                time.sleep(polling_interval)
                continue
            self.widget_params = new_widget_params
            time.sleep(polling_interval)



root = tk.Tk()
root.attributes("-alpha", 0.0)
manager = WindowManager(root)


class KeyEvent:
    key2wid = None
    key1 = None
    key2 = None

    @staticmethod
    def add_key(key):
        if key in KeyEvent.key2wid:
            KeyEvent.key1 = key
            manager.reset()
        else:
            if KeyEvent.key1 is None:
                KeyEvent.key1 = key
            else:
                KeyEvent.key2 = key
                manager.reset()


def handle_key_event():

    #wids = current_windows()
    #widgets = []
    #key2wid = {}
    #params = []
    #for j, wid in enumerate(wids):
    #    pos, size, name = win_pos(wid), win_size(wid), win_name(wid)
    #    if 'alttab.py' == name: continue
    #    if pos is None: continue
    #    if 'unity' in name: continue
    #    if 'tk' in name: continue
    #    if 'launcher' in name: continue
    #    if 'Desktop' in name: continue
    #    pos = list(pos)
    #    size = list(size)
    #    if pos[0] < 0 or pos[1] < 0: continue # todo: handle windows on other desktops
    #    if size is None: continue
    #    centerx = (pos[0]+size[0])-(size[0]/2)
    #    centery = (pos[1]+size[1])-(size[1]/2)
    #    params.append([centerx, centery, keys[j], wid, scan_codes[j], name])

    manager.event = True
    t.tick('full')
    params = copy.deepcopy(p.widget_params)
    p.key_event_start()
    if len(params) == 0:
        p.key_event_stop()
        return
    widgets = []
    coords = set()
    for x, y, key, wid, scan_code, name in params:
        while (x,y) in coords:
            y += 40
            x += 40
        coords.add((x,y))
        manager.move(key, x, y, name)
        manager.key2wid[key] = wid
    p.key_event_stop()
    manager.master.focus_force()


p = WindowPoller()
p.start()
keyboard.add_hotkey('ctrl+alt+k', handle_key_event)
root.mainloop()
