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

        self.display.show(self.splash)

        color_bitmap = displayio.Bitmap(128, 32, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        self.splash.append(bg_sprite)

        # Draw a smaller inner rectangle
        inner_bitmap = displayio.Bitmap(118, 24, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
        self.splash.append(inner_sprite)

        # Draw a label
        text = "Hello World!"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=15)
        self.splash.append(text_area)

