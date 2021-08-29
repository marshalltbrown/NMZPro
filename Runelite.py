from pywinauto.application import Application


class runelite:
    def __init__(self):

        self.client = Application().connect(path=r"C:\Users\Marshall\AppData\Local\RuneLite")['RuneLite']
        self.client_width = None
        self.client_height = None
        self.rectangle = None
        self.tab = 'Unknown'
        self.health = 'Unknown'
        self.eating = 'Pending'
        self.rect_alch = None
        self.rect_rapid_heal = None
        self.rect_rock_cake = None
        self.coord_login_entry = None
        self.coord_existing_user = None

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

        self.rect_alch = rectangle(self.getAbsoluteCoord(708, 365), self.getAbsoluteCoord(723, 349))
        self.rect_rapid_heal = rectangle(self.getAbsoluteCoord(706, 307), self.getAbsoluteCoord(733, 281))
        self.rect_rock_cake = rectangle(self.getAbsoluteCoord(571, 267), self.getAbsoluteCoord(594, 244))
        self.coord_login_entry = self.getAbsoluteCoord(350, 289)
        self.coord_existing_user = self.getAbsoluteCoord(395, 315)

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


class rectangle:
    def __init__(self, top_left, bottom_right):
        self.left = top_left[0]
        self.top = top_left[1]
        self.right = bottom_right[0]
        self.bottom = bottom_right[1]

