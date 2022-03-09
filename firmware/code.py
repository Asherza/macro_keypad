import board
import busio

from display_controller import display_controller
from hid_controller import hid_controller
from key_manager import key_manager


# This "enum" is used as a state machine pointer to know what mode of operation
# the keypad is in. Don't change these variables, they have no protection :)
class SM():
    init = 0            # init will do all the setup
    operation_mode = 1  # Normal mode of operation
    config_mode = 2     # Configuration mode



# Start the state_machine flag in init mode
state_machine_mode = SM.init

# Initalize the display, and the keypad with its default values
display = display_controller(board.GP1, board.GP0)
hid = hid_controller()

# Set up our key manager with the keys we want.
km = key_manager([board.GP10, board.GP11, board.GP12, board.GP13], 'default.cfg')

while True:
    print(km.read_key_switches())