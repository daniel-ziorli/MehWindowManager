import json
import keyboard
import subprocess
import pyautogui

config = {}
with open('config.json') as json_file:
    config = json.load(json_file)

pyautogui.PAUSE = config['key_press_delay']
meh_data = config['mehs']
for meh_key in meh_data:
    meh = meh_data[meh_key]
    meh['len'] = len(meh_key.split('+'))
    meh['split'] = meh_key.split('+')
    meh['is_pressed'] = False
hotkeys = config['hotkeys']

keys = []
meh_keys = []
for meh_key in meh_data:
    meh = meh_data[meh_key]
    keys.extend(meh['split'])
    meh_keys.extend(meh['split'])

for key in hotkeys.keys():
    keys.append(key)

keys = list(set(keys))
meh_keys = list(set(meh_keys))


def release_meh():
    for meh_key in meh_data:
        meh = meh_data[meh_key]
        for key in meh['split']:
            pyautogui.keyUp(key)


def hotkey_pressed(hot_key, process):
    release_meh()
    pyautogui.keyUp(hot_key)
    with pyautogui.hold('ctrl'):
        pyautogui.press('z')

    windows = pyautogui.getWindowsWithTitle(process['title'])

    print(windows)
    if len(windows) > 0:
        for window in windows:
            try:
                window.activate()
            except:
                window.minimize()
                window.restore()
    else:
        subprocess.Popen(process['path'])


def any_meh_pressed():
    for meh_key in meh_data:
        if meh_pressed(meh_data[meh_key]):
            return True
    return False


def meh_pressed(meh):
    if meh['can_toggle'] and meh['is_pressed']:
        return True
    for key in meh['split']:
        if not keyboard.is_pressed(key):
            return False
    return True


def key_pressed(KeyboardEvent):
    key = KeyboardEvent.name.lower()
    print('pressed ' + key)

    if key in meh_keys:
        return

    if not any_meh_pressed():
        return

    hotkey_pressed(key, hotkeys[key])
    for meh_key in meh_data:
        meh = meh_data[meh_key]
        meh['is_pressed'] = False


def key_released(KeyboardEvent):
    key = KeyboardEvent.name.lower()
    print('released ' + key)
    if key not in meh_keys:
        return

    if not meh_data[key]['can_toggle']:
        return
    meh_data[key]['is_pressed'] = not meh_data[key]['is_pressed']


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
