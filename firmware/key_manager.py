import json
from digitalio import DigitalInOut, Direction, Pull
from supervisor import ticks_ms

# This class is in charge or managing reading macro files
# and assigning key_switches
class key_manager():
    # key_list is a list of board pins that we want to assign our keys to
    # _default_key_cfg is the default config that we want to load on init
    # _debounce_time is an optional value that can be used to set the debounce time in ms
    def __init__(self, _key_list, _default_key_cfg, _debounce_time = 30):

        # Keeps track of the number of kew_switches this manager handles
        self._num_of_keys = len(_key_list)

        # default folder we will look in at the root of CIRCUITPY
        self._base_cfg_dir = 'switch_configs/'

        # Build our _switch_list with the default config and the pins _key_list provides
        self._switch_list = [key_switch(b, **k) for k, b in zip(self._parse_cfg_file(_default_key_cfg), _key_list)]

        # set debounce time for the entire key_manager
        self._km_debounce_time = _debounce_time

    # Parse a config file, this file HAS to have all key_switch macros defined
    # This returns a tuple of all the json objects that can be used to create key_switch objects.
    def _parse_cfg_file(self, cfg_file):

        # Empty dict to hold the parsed json.
        json_obj = {}

        # read the json file:
        with open(f'{self._base_cfg_dir}{cfg_file}', 'r') as f:
                json_obj = json.loads(f.read())

        # Return a list with the broken out switch json objects:
        # These are sorted by the 'id' key value pair, as this should support setting single keys, or less than the max amount
        return sorted([json_obj[key] for key in json_obj.keys()], key=lambda k: k['id'])

    # read_keys reads all the current keys in the _switch_list
    # this function returns all the switch statuses accounting for debounce time in a list
    def read_key_switches(self):
        return [sw.get_pin_state(self._km_debounce_time) for sw in self._switch_list]

# class that keeps hold of all the key data.
# This is a bit more easy to manage than a json object
class key_switch():
    def __init__(self,_board_pin, **kwargs):

        # Create a key that will keep track of the pin status
        self._key = DigitalInOut(_board_pin)

        # Set the direction of the pin to supply an input
        self._key.direction = Direction.INPUT

        # Set our pin with a pull up resistor
        self._key.pull = Pull.DOWN

        # Used to keep track of debounce
        self._last_debounce_time = ticks_ms()
        self._last_debounced_state = self._key.value
        self._last_debounced_reading_state = self._key.value

        # Assign all the kwargs to memeber variables, usually this would be done via __dict__.update() but
        # circuitpython does not support it
        for key, value in kwargs.items():
            setattr(self, "_" + key, value)

    # A getter function that will return debounced state values of the key_switch
    def get_pin_state(self, _debounce_time):

        # grab what the pin's state is in:
        reading = self._key.value

        # Check if the switch changed states since our last reading, if it has, update our last debounce time.
        if self._last_debounced_reading_state != reading:
            self._last_debounce_time = ticks_ms()

        # Check if switch_key has been in the same state for our elapsed _debounce_time
        if (ticks_ms() - self._last_debounce_time) > _debounce_time:
            # woo, its safe to read our value from the switch_key
            self._last_debounced_state = reading

        self._last_debounced_reading_state = reading

        # We can now return the debounced state, should be the correct state of the key_switch
        return self._last_debounced_state