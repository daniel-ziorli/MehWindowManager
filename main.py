import json
import keyboard
import subprocess
import pyautogui
import pywinctl as pwc

config = {}
with open('config.json') as json_file:
    config = json.load(json_file)

global meh_is_pressed, hooks
globals()['meh_is_pressed'] = False
globals()['hooks'] = []

pyautogui.PAUSE = config['key_press_delay']
meh = config['meh']
meh_split = meh.split('+')
meh_len = len(meh_split)
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


def execute_hotkey(hot_key, process):
    pyautogui.keyUp(hot_key)

    windows = pwc.getWindowsWithTitle(
        process['title'],
        condition=pwc.Re.CONTAINS,
        flags=pwc.Re.IGNORECASE
    )

    if len(windows) > 0:
        for window in windows:
            if config['debug']:
                print(window.title)
            window.activate()
    else:
        subprocess.Popen(process['path'])


def meh_pressed():
    if meh_can_toggle and globals()['meh_is_pressed']:
        return True
    for key in meh_split:
        if not keyboard.is_pressed(key):
            return False
    return True


def key_pressed(KeyboardEvent):
    key = KeyboardEvent.name.lower()

    if key in meh_keys:
        return

    if not meh_pressed():
        return

    execute_hotkey(key, hotkeys[key])
    globals()['meh_is_pressed'] = False
    unhook_all()


def meh_key_pressed(_):
    if not meh_pressed():
        return

    if len(globals()['hooks']) > 0:
        return

    for key in keys:
        hook = keyboard.on_press_key(
            key,
            key_pressed,
            suppress=True
        )
        globals()['hooks'].append(hook)


def meh_key_released(_):
    if not meh_can_toggle:
        return

    globals()['meh_is_pressed'] = not globals()['meh_is_pressed']
    if globals()['meh_is_pressed']:
        return
    unhook_all()


def unhook_all():
    for hook in globals()['hooks']:
        keyboard.unhook(hook)
    globals()['hooks'] = []


for key in meh_split:
    keyboard.on_press_key(
        key,
        meh_key_pressed,
    )
    keyboard.on_press_key(
        key,
        meh_key_released,
    )

if config['debug']:
    keyboard.on_press(
        lambda x: print(x.name.lower()),
    )

keyboard.wait()
