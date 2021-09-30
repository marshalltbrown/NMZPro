from pywinauto.application import Application
from enum import Enum
from utils import getTRNVCoord
from object_templates import *


class runelite:
    def __init__(self):
        print(f"Runelite virtual client instantiated.")
        # TODO clean up classes
        self.client = Application().connect(path=r"C:\Users\Marshall\AppData\Local\RuneLite")['RuneLite']


        # Usable vars
        self.rectangle = self.client.rectangle()
        self.offset = (self.rectangle.left, self.rectangle.top,)

        self.buffed = True
        self.absorbs = 0
        self.hp = 1
        self.inNMZ = True

        # Initializations & offsets
        self.inventory = self.init_inventory()
        # Updates offset for each inventory space
        for row in range(7):
            for column in range(4):
                self.inventory[row][column].set_offset(self.offset)

        # Update all enums found below
        for _coord in coordinates.__dict__.values():
            _coord.set_offset(self.offset)
        for _tab in tabs.__dict__.values():
            _tab.set_offset(self.offset)
        for _rect in rects.__dict__.values():
            _rect.set_rect(self.offset)

    def init_inventory(self):
        # 30 px wide then a 12px usable gap between boxes 42 total
        inventory = [[inv_slot((0, 0,), (0, 0,)) for row in range(4)] for column in range(7)]
        for row, t_b in enumerate(zip(range(244, 496, 36), range(267, 519, 36))):
            for column, l_r in enumerate(zip(range(568, 736, 42), range(597, 765, 42))):
                inventory[row][column] = inv_slot((l_r[0], t_b[0],), (l_r[1], t_b[1],))
        return inventory

    def get_items(self, item: str):
        items = []
        for row in range(7):
            for column in range(4):
                if item in self.inventory[row][column].contents:
                    items.append(getTRNVCoord(self.inventory[row][column].rect))
        return items

    def update_location(self) -> None:
        r = self.client.rectangle()
        top_left = (r.left, r.top,)
        if top_left != self.offset:
            bottom_right = (r.right, r.bottom,)
            # Updates client.rectangle
            self.rectangle = rectangle(top_left, bottom_right)
            # Updates client.offset
            self.offset = top_left

            # Updates offset for each inventory space
            for row in range(7):
                for column in range(4):
                    self.inventory[row][column].set_offset(top_left)

            # Update all enums found below
            for _tab in tabs.__dict__.values():
                _tab.set_offset(self.offset)
            for _coord in coordinates.__dict__.values():
                _coord.set_offset(self.offset)
            for _rect in rects.__dict__.values():
                _rect.set_rect(self.offset)

            print('Updated client')

    def setFocus(self) -> None:
        if self.client.exists():
            self.client.set_focus()


class tabs():

    inventory = tab('Inventory', (632, 196,), (658, 229,))
    prayer = tab('Prayer', (698, 196,), (724, 229,))
    magic = tab('Magic', (749, 196,), (784, 229,))
    logout = tab('Logout', (634, 497,), (660, 523,))


class rects():

    logout = rectangle((578, 445,), (708, 469,))
    quick_pray = rectangle((523, 107,), (571, 132,))
    alch = rectangle((708, 349,), (723, 365,))
    rapid_heal = rectangle((706, 281,), (733, 307,))
    melee_prayer = rectangle((671, 360,), (694, 380,))


class coordinates():
    pass_input_area = coord(350, 289)
    existing_user_login_box = coord(395, 315)
