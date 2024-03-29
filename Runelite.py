from typing import Optional
from pywinauto.application import Application
from utilities.object_templates import rectangle, tab, inv_slot


class runelite:
    def __init__(self):
        print(f"Runelite virtual client instantiated.")

        # Location vars
        self.client = Application().connect(path=r"C:\Users\Marshall\AppData\Local\RuneLite")['RuneLite']
        self.rectangle = self.client.rectangle()
        self.offset: tuple = (self.rectangle.left, self.rectangle.top,)

        # Vars
        self.current_tab: Optional[tab] = None
        self.buffed: bool = True
        self.absorbs: int = 0
        self.hp: int = 1
        self.inNMZ: bool = True
        self.overloaded: bool = False

        # Initializations & offsets
        self.inventory: [[inv_slot]] = self.init_inventory()
        rectangle.offset = self.offset

    @staticmethod
    def init_inventory() -> [[inv_slot]]:
        # 30 px wide then a 12px usable gap between boxes 42 total
        inventory = [[inv_slot((0, 0,), (0, 0,)) for row in range(4)] for column in range(7)]
        for row, t_b in enumerate(zip(range(244, 496, 36), range(267, 519, 36))):
            for column, l_r in enumerate(zip(range(568, 736, 42), range(597, 765, 42))):
                inventory[row][column] = inv_slot((l_r[0], t_b[0],), (l_r[1], t_b[1],))
        return inventory

    def get_item_locations(self, item: str) -> [rectangle]:
        items = []
        for row in range(7):
            for column in range(4):
                if item in self.inventory[row][column].contents:
                    items.append(self.inventory[row][column].rect.random_coord)
        return items

    def update_location(self) -> None:
        r = self.client.rectangle()
        self.rectangle = r
        top_left = (r.left, r.top,)
        if top_left != self.offset:
            bottom_right = (r.right, r.bottom,)
            # Updates client.rectangle
            self.rectangle = rectangle(top_left, bottom_right)
            # Updates client.offset
            self.offset = top_left

            # Updates vars and data class
            rectangle.offset = top_left

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
    existing_user = rectangle((399, 303,), (533, 334,))
    password_input = rectangle((346, 286,), (514, 298,))
