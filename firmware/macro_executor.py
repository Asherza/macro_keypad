import usb_hid

# import all required hid releated libs
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from adafruit_hid.mouse import Mouse
import time
import adafruit_ducky
class macro_executor():

    def __init__(self):
        # set up the mouse hid device
        self._mouse = Mouse(usb_hid.devices)

        #set up the keyboard:
        keyboard = Keyboard(usb_hid.devices)

        self._kb = KeyboardLayout(keyboard)

        # We're going to hack this library since it wants our 
        # DUCKY text in a text file, we're going to just pass it boot_out.txt
        self._duck = adafruit_ducky.Ducky(f"boot_out.txt", keyboard, self._kb)


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
                if command_name[0] == "DUCKY":
                    self._command_DUCKY(command_name[1:])

        return run_macro_str

    # This function will handle any DUCKY commands
    # TODO: Update Ducky commands to support a full ducky stack
    def _command_DUCKY(self, _ducky_list):
        # Manually set the lines for ducky, this is pretty hacky, but it should work pretty well!
        self._duck.lines = _ducky_list
        print(self._duck.lines)
        # Run the command :)
        self._duck.loop()

    # This function simpily takes the string that is passed from the macro and prints it out
    def _command_STRING(self, _string):
        print(f'Going to run {_string}')
        self._kb.write(_string)

    # Take in a string that is 3 indices where the first one is x,y,scroll
    # Where 20,0,0 would move mouse to the right +20 pixles, negative moves to the left
    # the scroll will scroll the mouse wheel a number of ticks
    def _command_MOVE_MOUSE(self, _string):
        # Lets take our string and convert it into ints, and pass it into mouse.move
        int_list = [int(i) if i != 0 else 0 for i in _string.split(',')]
        print(f'Going to move mouse {int_list}')
        self._mouse.move(int_list[0], int_list[1],int_list[2])
        time.sleep(.01)

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