import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode

# This class will control the hid commands
class hid_controller:

    def __init__(self):
        # Set up a keyboard device.
        self.kbd = Keyboard(usb_hid.devices)
        self.layout = KeyboardLayout(self.kbd)

    def send_hello_world(self):
        self.layout.write("Hello World!")
