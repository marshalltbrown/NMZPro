from pywinauto.application import Application


class runelite:
    def __init__(self):
        print(f"Runelite virtual client instantiated.")

        self.client = Application().connect(path=r"C:\Users\Marshall\AppData\Local\RuneLite")['RuneLite']
        self.offset = (self.client.rectangle().left, self.client.rectangle().top,)

        # Usable vars
        self.rectangle = self.client.rectangle()
        self.tab = 'Unknown'

        self.buffed = True
        self.absorbs = 999
        self.hp = 1

        self.inNMZ = True

        # Init Rectangles
        self.rect_inventory_tab = rectangle((632, 196,), (658, 229,), self.offset)
        self.rect_prayer_tab = rectangle((698, 196,), (724, 229,), self.offset)
        self.rect_magic_tab = rectangle((749, 196,), (784, 229,), self.offset)
        self.rect_logout_tab = rectangle((634, 497,), (660, 523,), self.offset)

        self.rect_logout_button = rectangle((578, 445,), (708, 469,), self.offset)
        self.rect_quick_pray = rectangle((523, 107,), (571, 132,), self.offset)
        self.rect_alch = rectangle((708, 349,), (723, 365,), self.offset)
        self.rect_rapid_heal = rectangle((706, 281,), (733, 307,), self.offset)
        self.rect_melee_prayer = rectangle((671, 360,), (694, 380,), self.offset)

        self.coord_login_entry = (350+self.offset[0], 289+self.offset[1],)
        self.coord_existing_user = (395+self.offset[0], 315+self.offset[1],)

        self.inventory = self.init_inventory()

    def update_location(self) -> None:
        r = self.client.rectangle()
        top_left = (r.left, r.top,)
        if top_left != self.offset:
            bottom_right = (r.right, r.bottom,)
            self.update(top_left, bottom_right)

    def check_pot(self, pot):
        pot_found = False
        for row in range(7):
            for column in range(4):
                if pot in self.inventory[row][column].contents:
                    pot_found = True
                    continue
        return pot_found

    def update(self, top_left, bottom_right) -> None:
        self.rectangle = rectangle(top_left, bottom_right, (0, 0,))
        self.offset = top_left
        self.update_rectangles(top_left)
        for row in range(7):
            for column in range(4):
                self.inventory[row][column].set_rect(top_left)
        print('Updated client')

    def setFocus(self) -> None:
        if self.client.exists():
            self.client.set_focus()

    def init_inventory(self):
        # 30 px wide then a 12px usable gap between boxes 42 total
        inventory = [[inv_slot((0, 0,), (0, 0,), (1, 1,)) for row in range(4)] for column in range(7)]
        for row, t_b in enumerate(zip(range(244, 496, 36), range(267, 519, 36))):
            for column, l_r in enumerate(zip(range(568, 736, 42), range(597, 765, 42))):
                inventory[row][column] = inv_slot((l_r[0], t_b[0],), (l_r[1], t_b[1],), self.offset)
        return inventory

    def update_rectangles(self, offset) -> None:
        self.rect_inventory_tab = rectangle((632, 196,), (658, 229,), offset)
        self.rect_prayer_tab = rectangle((698, 196,), (724, 229,), offset)
        self.rect_magic_tab = rectangle((749, 196,), (784, 229,), offset)
        self.rect_logout_tab = rectangle((634, 497,), (660, 523,), offset)

        self.rect_logout_button = rectangle((578, 445,), (708, 469,), offset)
        self.rect_quick_pray = rectangle((523, 107,), (571, 132,), offset)
        self.rect_alch = rectangle((708, 349,), (723, 365,), offset)
        self.rect_rapid_heal = rectangle((706, 281,), (733, 307,), offset)
        self.rect_melee_prayer = rectangle((671, 360,), (694, 380,), offset)

        self.coord_login_entry = (350+offset[0], 289+offset[1],)
        self.coord_existing_user = (395+offset[0], 315+offset[1],)


class inv_slot:
    def __init__(self, top_left, bottom_right, offset):
        self.tl = top_left
        self.br = bottom_right
        self.rect = rectangle(self.tl, self.br, offset)
        self.contents = '?'

    def set_rect(self, offset) -> None:
        self.rect = rectangle(self.tl, self.br, offset)


class rectangle:
    def __init__(self, top_left, bottom_right, offset):
        offset_x, offset_y = offset
        self.left = top_left[0] + offset_x
        self.top = top_left[1] + offset_y
        self.right = bottom_right[0] + offset_x
        self.bottom = bottom_right[1] + offset_y
        self.center = (((self.left + self.right) / 2), ((self.top + self.bottom) / 2),)
