from pywinauto.application import Application


class runelite:
    def __init__(self):
        print(f"Runelite virtual client instantiated.")

        self.client = Application().connect(path=r"C:\Users\Marshall\AppData\Local\RuneLite")['RuneLite']
        self.offset = (self.client.rectangle().left, self.client.rectangle().top,)
        self.training_style = 'R'  # Change this to S (Strength pot) or R (range pot)

        # Usable vars
        self.rectangle = self.client.rectangle()
        self.tab = 'Unknown'
        self.health = 'Unknown'
        self.absorption = 'Pending'
        self.buff = 'Pending'

        # Script vars
        self.eating = 'Pending'
        self.nmz_running = False
        self.flicking = False
        self.absorbs_remaining = True
        self.buffs_remaining = True
        self.inNMZ = True

        # Init Rectangles
        self.rect_alch = None
        self.rect_rapid_heal = None
        self.rect_rock_cake = None
        self.coord_login_entry = None
        self.coord_existing_user = None
        self.rect_styles_tab = None
        self.rect_levels_tab = None
        self.rect_quest_tab = None
        self.rect_inventory_tab = None
        self.rect_gear_tab = None
        self.rect_prayer_tab = None
        self.rect_magic_tab = None
        self.rect_logout_tab = None
        self.rect_logout_button = None
        self.rect_quick_pray = None

        self.inventory = self.init_inventory()

    def update(self):
        self.rectangle = self.client.rectangle()
        self.offset = (self.client.rectangle().left, self.client.rectangle().top,)
        self.update_rectangles(self.offset)
        for row in range(7):
            for column in range(4):
                self.inventory[row][column].set_rect(self.offset)

    def setFocus(self):
        if self.client.exists():
            self.client.set_focus()

    def init_inventory(self):
        # 30 px wide then a 12px usable gap between boxes 42 total
        inventory = [[None for row in range(4)] for column in range(7)]
        top = 244
        bottom = 267
        for row in range(7):
            left = 568
            right = 597
            for column in range(4):
                inventory[row][column] = inv_slot((left, top,), (right, bottom,), self.offset)
                left += 42
                right += 42
            top += 36
            bottom += 36
        return inventory

    def update_rectangles(self, offset):
        self.rect_styles_tab = rectangle((527, 196,), (562, 229,), offset)
        self.rect_levels_tab = rectangle((564, 196,), (599, 229,), offset)
        self.rect_quest_tab = rectangle((601, 196,), (634, 229,), offset)
        self.rect_inventory_tab = rectangle((632, 196,), (658, 229,), offset)
        self.rect_gear_tab = rectangle((675, 196,), (710, 229,), offset)
        self.rect_prayer_tab = rectangle((698, 196,), (724, 229,), offset)
        self.rect_magic_tab = rectangle((749, 196,), (784, 229,), offset)
        self.rect_logout_tab = rectangle((634, 497,), (660, 523,), offset)

        self.rect_logout_button = rectangle((578, 445,), (708, 469,), offset)
        self.rect_quick_pray = rectangle((523, 107,), (571, 132,), offset)
        self.rect_alch = rectangle((708, 349,), (723, 365,), offset)
        self.rect_rapid_heal = rectangle((706, 281,), (733, 307,), offset)
        self.rect_rock_cake = rectangle((571, 244,), (594, 267,), offset)

        self.coord_login_entry = (350+offset[0], 289+offset[1],)
        self.coord_existing_user = (395+offset[0], 315+offset[1],)


class inv_slot:
    def __init__(self, top_left, bottom_right, offset):
        self.tl = top_left
        self.br = bottom_right
        self.rect = self.set_rect(offset)
        self.contents = '?'

    def set_rect(self, offset):
        return rectangle(self.tl, self.br, offset)


class rectangle:
    def __init__(self, top_left, bottom_right, offset):
        offset_x, offset_y = offset
        self.left = top_left[0] + offset_x
        self.top = top_left[1] + offset_y
        self.right = bottom_right[0] + offset_x
        self.bottom = bottom_right[1] + offset_y
        self.center = (((self.left + self.right) / 2), ((self.top + self.bottom) / 2),)
