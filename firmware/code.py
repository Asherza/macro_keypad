
import board
import busio

from display_controller import display_controller
from hid_controller import hid_controller

display = display_controller(board.GP1, board.GP0)
hid = hid_controller()

while True:
    pass
