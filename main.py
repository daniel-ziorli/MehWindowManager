import json
import time
import keyboard
import subprocess
import pywinctl as pwc
from pynput import keyboard
from pynput.keyboard import Key, Controller

config = {}
with open('config.json') as json_file:
    config = json.load(json_file)

global key_listener, is_meh_pressed, ignore_toggle_release, windows, last_window_cache
globals()['last_window_cache'] = time.time()
globals()['windows'] = {}
globals()['is_meh_pressed'] = False
globals()['ignore_toggle_release'] = False

meh = config['meh']
hotkeys = config['hotkeys']
debug = config['debug']
can_toggle = config['can_toggle']
reset_toggle = config['reset_toggle']
cache_on_start = config['cache_on_start']
cache_rate = config['cache_rate']

for key in list(hotkeys):
    hotkeys[keyboard.KeyCode.from_char(key)] = hotkeys[key]
    del hotkeys[key]

def cache_titles():
    globals()['windows'] = {}
    all_windows = pwc.getAllWindows()

    for window in all_windows:
        globals()['windows'][window.title.lower()] = window

    if not debug:
        return
    print("all windows: ")
    for title in globals()['windows'].keys():
        print(title)


def execute_hotkey(key):
    controller.release(key)
    process = hotkeys[key]

    windows = []
    if not config['cache_on_start']:
        cache_titles()

    cached_windows = globals()['windows']
    for title in process['titles']:
        for window_title in cached_windows.keys():
            if title.lower() in window_title:
                windows.append(cached_windows[window_title])

    if len(windows) > 0:
        for window in windows:
            window.activate()
    elif 'path' in process.keys():
        try:
            subprocess.Popen(process['path'])
        except FileNotFoundError:
            print("File not found: " + process['path'])


controller = Controller()

meh_key_presses = {}
meh_parsed = keyboard.HotKey.parse(meh)
for key in meh_parsed:
    meh_key_presses[key] = False


def meh_pressed():
    if can_toggle and globals()['is_meh_pressed']:
        return True
    for key in meh_key_presses:
        if not meh_key_presses[key]:
            return False
    return True


def meh_released():
    for key in meh_key_presses:
        if meh_key_presses[key]:
            return False

    return True


def suppress_events(bool):
    globals()['key_listener']._suppress = bool


def on_key_press(key):
    globals()['ignore_toggle_release'] = False
    if debug:
        print(key)

    if key in meh_parsed:
        meh_key_presses[key] = True
        if meh_pressed():
            suppress_events(True)
        return

    if not meh_pressed():
        return

    if key not in hotkeys:
        return

    execute_hotkey(key)

    if cache_on_start and time.time() - globals()['last_window_cache'] > cache_rate:
        if debug:
            print(time.time() - globals()['last_window_cache'] ,"s passed, caching titles")
        cache_titles()
        globals()['last_window_cache'] = time.time()

    if can_toggle and reset_toggle:
        globals()['is_meh_pressed'] = False
        globals()['ignore_toggle_release'] = True

    if not meh_pressed():
        suppress_events(False)


def on_key_released(key):
    if key not in meh_parsed:
        return

    meh_key_presses[key] = False

    if can_toggle and meh_released() and not globals()['ignore_toggle_release']:
        globals()['is_meh_pressed'] = not globals()['is_meh_pressed']

    if not meh_pressed():
        suppress_events(False)

if cache_on_start:
    cache_titles()
with keyboard.Listener(on_press=on_key_press, on_release=on_key_released) as listener:
    globals()['key_listener'] = listener
    listener.join()
