# MehWindowManager
## Description
MehWindowManager is a Python project that provides a simple window manager, allowing you to quickly switch between different applications using custom hotkeys. The term "meh" refers to the combination of keys used to trigger the window manager, meh normally refers to Ctrl + Alt + Shift by default but can be remapped according to your preferences.

## Configuration
The configuration file config.json allows you to customize various aspects of MehWindowManager:

### Parameters
**debug**: Set to true to enable debug mode, which provides additional logging information. Default is false.
**can_toggle**: Set to true to allow toggling between windows of the same application. Default is true.
**reset_toggle**: Set to true to reset the toggle state after the toggle timeout. Default is true.
**toggle_timeout**: Time in seconds before the toggle state resets. Default is 1.5.
**meh**: Key combination to trigger a window switch.
This program uses pynput to monitor keyboard inputs and all the valid keycodes can be found [here](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key).
You can also have a multi keycode meh by adding + between each keycode 
`<ctrl_l>+<alt_l>+<shift_l>`
**hotkeys**: Dictionary containing hotkey configurations. Each key corresponds to a single hotkey and its associated application. Pressing the meh key + the hotkey will open the given program. All the valid keycodes can be found [here](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key).

## Usage
1. Clone MehWindowManager 
`git clone https://github.com/daniel-ziorli/MehWindowManager.git`
2. Customize the config.json file according to your preferences
3. `python main.py`
