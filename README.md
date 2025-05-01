# MehWindowManager
## Description
MehWindowManager is a simple window manager, allowing you to quickly switch between different applications using custom hotkeys. The term "meh" refers to the combination of keys used to trigger the window manager, meh normally refers to Ctrl + Alt + Shift by default but can be remapped according to your preferences.

## Usage
1. Clone MehWindowManager 
`git clone https://github.com/daniel-ziorli/MehWindowManager.git`
2. Customize the config.json file according to your preferences
3. `python main.py`

## Configuration
The configuration file config.json allows you to customize various aspects of MehWindowManager:

### Parameters
**debug**: Set to true to enable debug mode, which provides additional logging information, it's helpful for getting keycodes. Default is false.

**can_toggle**: Set to true to allow toggling of the meh key. Default is true.

**reset_toggle**: Set to true to reset the toggle state after a hotkey is activated. Default is true.

**toggle_timeout**: Time in seconds before the toggle state resets. Default is 1.5.

**meh**: Key combination to trigger a window switch.
This program uses pynput to monitor keyboard inputs and all the valid keycodes can be found [here](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key).
You can also have a multi keycode meh by adding + between each keycode 
`<ctrl_l>+<alt_l>+<shift_l>`

**hotkeys**: Dictionary containing hotkey configurations. Each key corresponds to a single hotkey and its associated application. Pressing the meh key + the hotkey will open the given program. All the valid keycodes can be found [here](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key).
