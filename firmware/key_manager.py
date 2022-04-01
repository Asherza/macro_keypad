import json
from key_switch import key_switch

# This class is in charge or managing reading macro files
# and assigning key_switches
class key_manager():
    # key_list is a list of board pins that we want to assign our keys to
    # _default_key_cfg is the default config that we want to load on init
    # _debounce_time is an optional value that can be used to set the debounce time in ms
    def __init__(self, _key_list, _default_key_cfg, _macro_executor, _debounce_time = 30):

        # Keeps track of the number of kew_switches this manager handles
        self._num_of_keys = len(_key_list)

        # default folder we will look in at the root of CIRCUITPY
        self._base_cfg_dir = 'switch_configs/'

        # Create a macro executor
        self._macro_exe = _macro_executor

        # Build our _switch_list with the default config and the pins _key_list provides
        self._switch_list = [key_switch(b, 'down', **k) for k, b in zip(self._parse_cfg_file(_default_key_cfg), _key_list)]

        # lets set up a last known state of our switches, we will use this later to manage if someone is holding a button down
        [ks.set_var(last_state = False) for ks in self._switch_list]

        # set the key_switches to their macros
        self.set_key_switches_to_macro()

        # set debounce time for the entire key_manager
        self._km_debounce_time = _debounce_time

    # Lets scan our switches and run any functions they have if the key_switch has a value of true (held down)
    def scan_and_run_switches(self):
        for ks in self._switch_list:
            # Grab the state of the ks.
            ks_state = ks.get_debounced_pin_state(self._km_debounce_time)

            # Only run the function if our last ks.state was false and we see a high
            # (User has just pressed the button, but we will not trigger if its held)
            if ks.get_var(['last_state']) == False and ks_state == True:
                ks.run_func()
                ks.set_var(last_state = ks_state)
            else:
                ks.set_var(last_state = ks_state)


    # This function will set the key_switches it manages to use their macro functions
    def set_key_switches_to_macro(self):
        # loop through the key_switches:
        for key_switch in self._switch_list:
            # Set the key_switch function to the macro_exe function
            # lets first gen a new function with the key_switches set macro
            func = self._macro_exe.gen_macro_func(key_switch.get_var(['macro']))
            # Set the key_switch to use the new macro func we created
            key_switch.set_func(func)

    # read_keys reads all the current keys in the _switch_list
    # this function returns all the switch statuses accounting for debounce time in a list
    def read_key_switches(self):
        return [sw.get_debounced_pin_state(self._km_debounce_time) for sw in self._switch_list]

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



