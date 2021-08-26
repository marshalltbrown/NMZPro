from pywinauto.application import Application


class runelite:
    def __init__(self):
        self.client = Application().connect(path=r"C:\Users\Marshall\AppData\Local\RuneLite")['RuneLite']
        self.client_width = None
        self.client_height = None
        self.client_rectangle = None
        self.tab = 'Unknown'
        self.health = 'Unknown'
        self.eating = 'Pending'
        self.updateClient()
        print(f"Runelite instantiated with window coordinates: {self.client_rectangle}")

    def updateClient(self):
        self.client_rectangle = self.client.rectangle()
        if self.client_rectangle.right - self.client_rectangle.left > 1001:
            self.client_width = self.client_rectangle.right - self.client_rectangle.left - 242
            # Runelite options are open. Shrinking perceived window width to compensate.
        else:
            self.client_width = self.client_rectangle.right - self.client_rectangle.left
        self.client_height = self.client_rectangle.bottom - self.client_rectangle.top

    def getX(self, formula):
        return round(self.client_rectangle.left + (self.client_width * formula))

    def getY(self, formula):
        return round(self.client_rectangle.bottom - (self.client_height * formula))

    def setFocus(self):
        if self.client.exists():
            self.client.set_focus()
