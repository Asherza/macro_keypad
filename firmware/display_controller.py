import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import busio

# This class is used to drive the lcd display
class display_controller:
    # Init the display and object
    def __init__(self, i2c_SCL_pin, i2c_SDA_pin):

        displayio.release_displays()

        i2c = busio.I2C(i2c_SCL_pin, i2c_SDA_pin)

        display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

        self.display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

        self.splash = displayio.Group()

        self.draw_hello_world()

    def draw_hello_world(self):

        # Setup the file as the bitmap data source
        self.bitmap = displayio.OnDiskBitmap("/basic_menu.bmp")

        # Create a TileGrid to hold the bitmap
        self.tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.bitmap.pixel_shader)

        # Create a Group to hold the TileGrid
        self.group = displayio.Group()

        # Add the TileGrid to the Group
        self.group.append(self.tile_grid)

        text_area = label.Label(terminalio.FONT, text="Hello Line 0", color=0xFFFFFF)
        text_area.x = 0
        text_area.y = 4
        text_area.anchor_point = (0.1, 0.8)

        text_area2 = label.Label(terminalio.FONT, text="Hello Line 1", color=0xFFFFFF)
        text_area2.x = 0
        text_area2.y = 14
        text_area2.anchor_point = (0.1, 0.8)
        self.group.append(text_area)
        self.group.append(text_area2)
        # Add the Group to the Display
        self.display.show(self.group)
