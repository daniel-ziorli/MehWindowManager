from multiprocessing import Process
import platform
import json
import time
import keyboard
import subprocess
import pywinctl as pwc
from pynput import keyboard
from pynput.keyboard import Controller

config = {}
with open('config.json') as json_file:
    config = json.load(json_file)

global key_listener, is_meh_pressed, ignore_toggle_release, previous_hotkey, toggle_time
globals()['previous_hotkey'] = None
globals()['is_meh_pressed'] = False
globals()['ignore_toggle_release'] = False
globals()['toggle_time'] = time.time()

meh = config['meh']
hotkeys = config['hotkeys']
debug = config['debug']
can_toggle = config['can_toggle']
reset_toggle = config['reset_toggle']
toggle_timeout = config['toggle_timeout']
platform_name = platform.system()

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

    
def execute_mac_hotkey(key):
    process = hotkeys[key]
    if 'mac_path' not in process.keys():
        return

    if key == globals()['previous_hotkey']:
        controller.press(keyboard.Key.cmd)
        controller.tap('`')
        controller.release(keyboard.Key.cmd)
    else:
        subprocess.call(["/usr/bin/open", "-a", process['mac_path']]),

    globals()['previous_hotkey'] = key


def execute_hotkey(key):
    process = hotkeys[key]
    windows = pwc.getWindowsWithTitle(
        process['title'],
        condition=pwc.Re.CONTAINS,
        flags=pwc.Re.IGNORECASE
    )

    if len(windows) > 0:
        for window in windows:
            if debug:
                print(window.title)
            window.activate()
    elif process['path'] is not None:
        subprocess.Popen(process['path'])


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

def darwin_intercept(event_type, event):
    if globals()['key_listener']._suppress:
        if not meh_pressed():
            suppress_events(False)
        return None
    else:
        return event

def suppress_events(bool):
    globals()['key_listener']._suppress = bool

def on_key_press(key):
    globals()['ignore_toggle_release'] = False
    if debug:
        print(key)

    if toggle_timeout != -1 and time.time() - globals()['toggle_time'] > toggle_timeout and globals()['is_meh_pressed']:
        reset_meh(key)
        return

    if key in meh_parsed:
        meh_key_presses[key] = True
        if meh_pressed():
            suppress_events(True)
        return

    if not meh_pressed():
        return

    if key not in hotkeys:
        reset_meh(key)
        return

    controller.release(key)
    if platform_name == 'Darwin':
        execute_mac_hotkey(key)
    else:
        execute_hotkey(key)

    if can_toggle and reset_toggle:
        globals()['is_meh_pressed'] = False
        globals()['ignore_toggle_release'] = True

    if not meh_pressed() and platform_name != 'Darwin':
        suppress_events(False)


def reset_meh(key):
    globals()['is_meh_pressed'] = False
    suppress_events(False)
    controller.tap(key)


def on_key_released(key):
    if key not in meh_parsed:
        return

    meh_key_presses[key] = False

    if can_toggle and meh_released() and not globals()['ignore_toggle_release']:
        globals()['is_meh_pressed'] = not globals()['is_meh_pressed']
        globals()['toggle_time'] = time.time()

    if not meh_pressed():
        suppress_events(False)

if platform_name == 'Darwin':
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_released, darwin_intercept=darwin_intercept) as listener:
        globals()['key_listener'] = listener
        listener.join()
else:
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_released) as listener:
        globals()['key_listener'] = listener
        listener.join()
