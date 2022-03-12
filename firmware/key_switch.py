from digitalio import DigitalInOut, Direction, Pull
from supervisor import ticks_ms

# class that keeps hold of all the key data.
# This is a bit more easy to manage than a json object
# Key_switch should be a generic class that a user can design around
class key_switch():
    # _board_pin is a circuitpython board pin
    # _Pull is a string that can be 'up', 'down', this sets the pull direction of the pin
    # **kwargs is any key:pair that you would like this key_switch to keep track of
    def __init__(self,_board_pin, _pull, **kwargs):

        # Create a key that will keep track of the pin status
        self._key = DigitalInOut(_board_pin)

        # Set the direction of the pin to supply an input
        self._key.direction = Direction.INPUT

        # Set our pin with a pull resistor passed in from the user
        self._key.pull = Pull.UP if _pull == 'up' else Pull.DOWN

        # Used to keep track of debounce
        self._last_debounce_time = ticks_ms()
        self._last_debounced_state = self._key.value
        self._last_debounced_reading_state = self._key.value

        # Assign all the kwargs to memeber variables, usually this would be done via __dict__.update() but
        # circuitpython does not support it
        for key, value in kwargs.items():
            setattr(self, key, value)

    # A getter function that will return debounced state values of the key_switch
    # This function takes in a _debounce_time that is in ms.
    def get_debounced_pin_state(self, _debounce_time):

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

    # set_var takes in a dictionary of kwargs and sets them all to memeber variables of the key_switch
    # Note that there is no protection of overwriting current variables if they exist, so be safe!
    def set_var(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Returns a dict of the key_value pairs that were asked for
    # the arg_list should be a list of key strings that a user wants to request,
    # If arg_list is not passed or passed as None, this function will return its entire self dict
    def get_var(self, arg_list = []):

        return_list = []

        # Look at every key the user passed
        for key in arg_list:
            # Grab the key if it exists, if not, lets not add it
            key_val_to_add = self.__dict__.get(key, None)

            # If our value ended up being None, then we will just add it anyways and let other handle it
            return_list.append(key_val_to_add)

        # return the list we filled, but if arg_list is passed as None, we just return the self.__dict__ of this key_switch
        return return_list if len(arg_list) > 0 else self.__dict__

    # this function allows the user to set the function of the key_switch
    # This replaces the func that is currently set for the key_switch
    def set_func(self, _func):
        self.func = _func

    # lets the user run the func that was set with set_func.
    # This function will send the *args and **kwargs to the func in case a user wants to pass
    # any params to the function
    def run_func(self, *args, **kwargs):
        return self.func(*args, **kwargs)

