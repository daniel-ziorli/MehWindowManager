import json
import keyboard
import subprocess
import pyautogui

config = {}
with open('config.json') as json_file:
    config = json.load(json_file)

pyautogui.PAUSE = config['key_press_delay']
meh = config['meh']
meh_len = len(meh)
meh_split = meh.split('+')
global meh_is_pressed
globals()['meh_is_pressed'] = False
meh_can_toggle = config['can_toggle']
hotkeys = config['hotkeys']

keys = []
meh_keys = []

keys.extend(meh_split)
meh_keys.extend(meh_split)

for key in hotkeys.keys():
    keys.append(key)

keys = list(set(keys))
meh_keys = list(set(meh_keys))


def release_meh():
    for key in meh_split:
        pyautogui.keyUp(key)


def hotkey_pressed(hot_key, process):
    release_meh()
    pyautogui.keyUp(hot_key)
    with pyautogui.hold('ctrl'):
        pyautogui.press('z')

    windows = pyautogui.getWindowsWithTitle(process['title'])

    if len(windows) > 0:
        for window in windows:
            try:
                window.activate()
            except:
                window.minimize()
                window.restore()
    else:
        subprocess.Popen(process['path'])


def meh_pressed():
    if meh_can_toggle and meh_is_pressed:
        return True
    for key in meh_split:
        if not keyboard.is_pressed(key):
            return False
    return True


def key_pressed(KeyboardEvent):
    key = KeyboardEvent.name.lower()
    print('pressed ' + key)

    if key in meh_keys:
        return

    if not meh_pressed():
        return

    hotkey_pressed(key, hotkeys[key])
    for key in meh_split:
        globals()['meh_is_pressed'] = False


def key_released(KeyboardEvent):
    key = KeyboardEvent.name.lower()
    print('released ' + key)
    if key not in meh_keys:
        return

    if not meh_can_toggle:
        return
    globals()['meh_is_pressed'] = not globals()['meh_is_pressed']


for key in keys:
    keyboard.on_press_key(
        key,
        key_pressed
    )

    keyboard.on_release_key(
        key,
        key_released
    )

keyboard.wait()
