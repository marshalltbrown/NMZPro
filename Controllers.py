from utilities.utils import WindMouse
from utilities.vars import settings
from Runelite import runelite
from tkinter import StringVar
import tkinter.scrolledtext


class admin:
    def __init__(self, style, strings, lock, inventory_strings, **kwargs):
        # TODO: Add gui class to better control gui strings
        # TODO clean up classes
        # Set initialization vars
        self.style = style  # Currently uses 'S' (Strength pot) or 'R' (range pot)
        self.gui = gui(strings, inventory_strings)
        self.lock = lock
        self.inv_strings = inventory_strings
        self.mouse = WindMouse(settings)

        for key, value in kwargs.items():
            setattr(self, key, value)

        # Static control vars
        self.active = True
        self.overloaded = False


class gui:
    def __init__(self, strings: dict, inventory: [[StringVar]]):

        self.hp: StringVar = strings['health']
        self.status: StringVar = strings['status']
        self.absorbs: StringVar = strings['absorption']
        self.buff: StringVar = strings['buff']
        self.tab: StringVar = strings['inventory']
        self.scroll_box: tkinter.scrolledtext = strings['box']
        self.inventory: [[StringVar]] = inventory

    def post(self, message) -> None:
        box = self.scroll_box
        fully_scrolled_down = box.yview()[1] == 1.0
        box.insert('end', message + "\n")
        if fully_scrolled_down:
            box.see("end")

    def refresh_inventory(self, client: runelite) -> None:

        self.buff.set(str(client.buffed))

        self.tab.set(client.current_tab.name)

        for row in range(7):
            for column in range(4):
                contents = client.inventory[row][column].contents
                doses = client.inventory[row][column].pot_doses
                if doses == 0:
                    self.inventory[row][column].set(contents)
                else:
                    self.inventory[row][column].set(f"{contents}{doses}")

