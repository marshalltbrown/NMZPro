from pywinauto.application import Application


class runelite:
    def __init__(self):

        self.client = Application().connect(path=r"C:\Users\Marshall\AppData\Local\RuneLite")['RuneLite']
        self.training_style = 'R'  # Change this to S (Strength pot) or R (range pot)
        self.client_width = None
        self.client_height = None
        self.rectangle = None
        self.tab = 'Unknown'
        self.health = 'Unknown'
        self.eating = 'Pending'
        self.absorption = 'Pending'
        self.buff = 'Pending'
        self.nmz_running = False
        self.flicking = False
        self.win32ui_window = True
        self.absorbs_remaining = True
        self.buffs_remaining = True
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
        self.inNMZ = True
        self.table_inventory_rects = [{}, {}, {}, {}, {}, {}, {}]

        self.update()
        print(f"Runelite instantiated with window coordinates: {self.rectangle}")

    def update(self):
        self.rectangle = self.client.rectangle()
        if self.rectangle.right - self.rectangle.left > 1001:
            self.client_width = self.rectangle.right - self.rectangle.left - 242
            # Runelite options are open. Shrinking perceived window width to compensate.
        else:
            self.client_width = self.rectangle.right - self.rectangle.left
        self.client_height = self.rectangle.bottom - self.rectangle.top

        self.rect_alch = rectangle(self.getAbsoluteCoord(708, 349), self.getAbsoluteCoord(723, 365))
        self.rect_rapid_heal = rectangle(self.getAbsoluteCoord(706, 281), self.getAbsoluteCoord(733, 307))
        self.rect_rock_cake = rectangle(self.getAbsoluteCoord(571, 244), self.getAbsoluteCoord(594, 267))
        self.coord_login_entry = self.getAbsoluteCoord(350, 289)
        self.coord_existing_user = self.getAbsoluteCoord(395, 315)
        self.updateTabLocations()
        self.updateInventoryLocations()

    def getX(self, formula):
        return round(self.rectangle.left + (self.client_width * formula))

    def getY(self, formula):
        return round(self.rectangle.bottom - (self.client_height * formula))

    def getAbsoluteCoord(self, x, y):
        x += self.rectangle.left
        y += self.rectangle.top
        return x, y

    def setFocus(self):
        if self.client.exists():
            self.client.set_focus()

    def updateInventoryLocations(self):
        # 30 px wide then a 12px usable gap between boxes 42 total
        top = 244
        bottom = 267
        for row in range(7):
            left = 568
            right = 597
            for column in range(4):
                self.table_inventory_rects[row][column] = rectangle(self.getAbsoluteCoord(left, top),
                                                                    self.getAbsoluteCoord(right, bottom))
                left += 42
                right += 42
            top += 36
            bottom += 36

    def updateTabLocations(self):
        # Rects have a usable width of 35 px with a 2px border.
        self.rect_styles_tab = rectangle(self.getAbsoluteCoord(527, 196), self.getAbsoluteCoord(562, 229))
        self.rect_levels_tab = rectangle(self.getAbsoluteCoord(564, 196), self.getAbsoluteCoord(599, 229))
        self.rect_quest_tab = rectangle(self.getAbsoluteCoord(601, 196), self.getAbsoluteCoord(634, 229))
        self.rect_inventory_tab = rectangle(self.getAbsoluteCoord(632, 196), self.getAbsoluteCoord(658, 229))
        self.rect_gear_tab = rectangle(self.getAbsoluteCoord(675, 196), self.getAbsoluteCoord(710, 229))
        self.rect_prayer_tab = rectangle(self.getAbsoluteCoord(698, 196), self.getAbsoluteCoord(724, 229))
        self.rect_magic_tab = rectangle(self.getAbsoluteCoord(749, 196), self.getAbsoluteCoord(784, 229))
        self.rect_logout_tab = rectangle(self.getAbsoluteCoord(634, 497), self.getAbsoluteCoord(660, 523))
        self.rect_logout_button = rectangle(self.getAbsoluteCoord(578, 445), self.getAbsoluteCoord(708, 469))
        self.rect_quick_pray = rectangle(self.getAbsoluteCoord(523, 107), self.getAbsoluteCoord(571, 132))


class rectangle:
    def __init__(self, top_left, bottom_right):
        self.left = top_left[0]
        self.top = top_left[1]
        self.right = bottom_right[0]
        self.bottom = bottom_right[1]
        self.center = (((self.left + self.right) / 2), ((self.top + self.bottom) / 2),)
