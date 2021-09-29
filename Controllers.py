

class admin:
    def __init__(self, style, strings, lock, inventory_strings, **kwargs):
        # TODO: Add gui class to better control gui strings
        # TODO clean up classes
        # Set initialization vars
        self.style = style  # Currently uses 'S' (Strength pot) or 'R' (range pot)
        self.strings = strings
        self.lock = lock
        self.inv_strings = inventory_strings

        for key, value in kwargs.items():
            setattr(self, key, value)

        # Static control vars
        self.active = True
        self.eating = False
        self.flicking = False
        self.drinking_absorbs = False
        self.drinking_buff = False
        self.overloading = False
        self.overload_time_left = 300
        self.overloaded = False
        self.moving_soon = {'buff': False,
                            'absorb': False,
                            'flicking': False,
                            'eating': False
                            }

        # for key, value in self.__dict__.items():
        #     print(f"K: {key}, V: {value}")
    def check_moving_soon(self):
        result = False
        if True in self.moving_soon.values():
            result = True
        return result

    def post(self, message):
        box = self.strings['box']
        fully_scrolled_down = box.yview()[1] == 1.0

        box.insert('end', message + "\n")
        if fully_scrolled_down:
            box.see("end")
