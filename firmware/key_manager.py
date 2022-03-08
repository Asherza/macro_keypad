import json
from digitalio import DigitalInOut, Direction, Pull


# This class is in charge or managing reading macro files
# and assigning key_switches
class key_manager():
    # key_list is a list of board values
    def __init__(self, _key_list, _default_key_cfg):

        # default folder we will look in at the root of CIRCUITPY
        self.base_cfg_dir = 'switch_configs/'

        # Use the default config to create 4 key_switch objects
        self.switch_list = [key_switch(**k) for k in self._parse_cfg_file(_default_key_cfg)]

        print(self.switch_list)

    # Parse a config file, this file HAS to have all 4 key_switch macros
    # This returns a tuple of four json objects that can be used to create key_switch objects.
    def _parse_cfg_file(self, cfg_file):
        # Empty dict to hold the parsed json.
        json_obj = {}

        # read the json file:
        with open(f'{self.base_cfg_dir}{cfg_file}', 'r') as f:
                json_obj = json.loads(f.read())

        # Return the tuple with the broken out switch json objects:
        return (json_obj['sw_0'], json_obj['sw_1'], json_obj['sw_2'], json_obj['sw_3'])

# class that keeps hold of all the key data.
# This is a bit more easy to manage than a json object
class key_switch():
    def __init__(self, **kwargs):
        # Assign all the kwargs to memeber variables, usually this would be done via __dict__.update() but
        # circuitpython does not support it
        for key, value in kwargs.items():
            setattr(self, key, value)

