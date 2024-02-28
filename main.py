import json
import keyboard
import subprocess
import pywinctl as pwc
from pynput import keyboard
from pynput.keyboard import Key, Controller

config = {}
with open('config.json') as json_file:
    config = json.load(json_file)

global key_listener, is_meh_pressed, ignore_toggle_release
globals()['is_meh_pressed'] = False
globals()['ignore_toggle_release'] = False

meh = config['meh']
hotkeys = config['hotkeys']
debug = config['debug']
can_toggle = config['can_toggle']
reset_toggle = config['reset_toggle']

for key in list(hotkeys):
    hotkeys[keyboard.KeyCode.from_char(key)] = hotkeys[key]
    del hotkeys[key]


def execute_hotkey(key):
    controller.release(key)
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
    else:
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


def suppreses_events(bool):
    globals()['key_listener']._suppress = bool


def on_key_press(key):
    globals()['ignore_toggle_release'] = False
    if debug:
        print(key)

    if key in meh_parsed:
        meh_key_presses[key] = True
        if meh_pressed():
            suppreses_events(True)
        return

    if not meh_pressed():
        return

    if key not in hotkeys:
        return

    execute_hotkey(key)
    if can_toggle and reset_toggle:
        globals()['is_meh_pressed'] = False
        globals()['ignore_toggle_release'] = True
    suppreses_events(False)


def on_key_released(key):
    if key not in meh_parsed:
        return

    meh_key_presses[key] = False

    if can_toggle and meh_released() and not globals()['ignore_toggle_release']:
        globals()['is_meh_pressed'] = not globals()['is_meh_pressed']

    if not meh_pressed():
        suppreses_events(False)


with keyboard.Listener(on_press=on_key_press, on_release=on_key_released) as listener:
    globals()['key_listener'] = listener
    listener.join()
