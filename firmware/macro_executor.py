# Some functions and ideas for this file were inspired by
# The pico-ducky repo found here https://github.com/dbisu/pico-ducky

import usb_hid

# import all required hid releated libs
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from adafruit_hid.mouse import Mouse

class macro_executor():

    def __init__(self):
        # set up the mouse hid device
        self._mouse = Mouse(usb_hid.devices)

        #set up the keyboard:
        keyboard = Keyboard(usb_hid.devices)

        self._kb = KeyboardLayout(keyboard)

        # anything thing in this list can simpily be ran via the hid command
        self._commands = {
            'WINDOWS': Keycode.WINDOWS, 'GUI': Keycode.GUI,
            'APP': Keycode.APPLICATION, 'MENU': Keycode.APPLICATION, 'SHIFT': Keycode.SHIFT,
            'ALT': Keycode.ALT, 'CONTROL': Keycode.CONTROL, 'CTRL': Keycode.CONTROL,
            'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,
            'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,
            'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,
            'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,
            'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,
            'INSERT': Keycode.INSERT, 'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'PAGEUP': Keycode.PAGE_UP,
            'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,
            'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB,
            'BACKSPACE': Keycode.BACKSPACE,
            'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
            'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
            'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
            'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
            'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
            'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
            'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,
            'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,
            'F12': Keycode.F12,
        }

    # This function takes in a macro_str and returns a function that can be used to execute the macro
    def gen_macro_func(self, _macro_str):

        def run_macro_str():
            # In the macro, we should break each command up by using the a ';' char and loop over them
            for command in _macro_str.split(';'):

                # lets grab the command within this macro,
                command_name = command.split(' ')
                print(command_name)
                # parse the commands and run the correct functions
                if command_name[0] == "STRING":
                    self._command_STRING(command_name[1])
                if command_name[0] == "MOUSE_MOVE":
                    self._command_MOVE_MOUSE(command_name[1])
                if command_name[0] == "MOUSE_CLICK":
                    self._command_MOUSE_CLICK(command_name[1])

        return run_macro_str

    # This function simpily takes the string that is passed from the macro and prints it out
    def _command_STRING(self, _string):
        print(f'Going to run {_string}')
        self._kb.write(_string)

    # Take in a string that is 3 indices where the first one is x,y,scroll
    # Where 20,0,0 would move mouse to the right +20 pixles, negative moves to the left
    # the scroll will scroll the mouse wheel a number of ticks
    def _command_MOVE_MOUSE(self, _string):
        # Lets take our string and convert it into ints, and pass it into mouse.move
        int_list = [int(i) for i in _string.split(',')]
        print(f'Going to move mouse {int_list}')
        self._mouse.move(*int_list)

    # Take in a string that is either l,r,m which represents
    # Click left mouse button, right mouse button, or middle
    def _command_MOUSE_CLICK(self, _string):
        if _string == 'l':
            self._mouse.click(Mouse.LEFT_BUTTON)
        elif _string == 'r':
            self._mouse.click(Mouse.RIGHT_BUTTON)
        elif _string == 'm':
            self._mouse.click(Mouse.MIDDLE_BUTTON)
        else:
            print("String passed to MOUSE_CLICK was not l,r, or m")