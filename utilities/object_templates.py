import random


class tab:
    def __init__(self, top_left: tuple, bottom_right: tuple, name: str = "Unknown", f_key: str = ''):
        self.name: str = name
        self.selected: bool
        self.rect: rectangle = rectangle(top_left, bottom_right)
        self.f_key: str = f_key


class rectangle:
    offset: tuple

    def __init__(self, top_left: tuple, bottom_right: tuple):
        self.left_static: float = top_left[0]
        self.top_static: float = top_left[1]
        self.right_static: float = bottom_right[0]
        self.bottom_static: float = bottom_right[1]

    @property
    def left(self) -> int:
        return self.left_static + rectangle.offset[0]

    @property
    def top(self) -> int:
        return self.top_static + rectangle.offset[1]

    @property
    def right(self) -> int:
        return self.right_static + rectangle.offset[0]

    @property
    def bottom(self) -> int:
        return self.bottom_static + rectangle.offset[1]

    @property
    def top_left_coord(self) -> tuple:
        return self.left, self.top

    @property
    def bottom_right_coord(self) -> tuple:
        return self.right, self.bottom

    @property
    def center_coord(self) -> tuple:
        """Returns the coordinate at the dead center of the rectangle."""
        return ((self.left + self.right) / 2), ((self.top + self.bottom) / 2),

    @property
    def random_coord(self) -> tuple:
        """Returns a normally distributed random coordinate truncated so it is within the rectangle box."""
        mean_x = (self.right + self.left) / 2
        mean_y = (self.top + self.bottom) / 2
        x = False
        y = False

        while x < self.left or x > self.right:
            x = random.normalvariate(mean_x, (self.right - self.left) / 4)

        while y < self.top or y > self.bottom:
            y = random.normalvariate(mean_y, (self.bottom - self.top) / 4)

        return x, y


class inv_slot:
    def __init__(self, top_left: tuple, bottom_right: tuple):
        self.tl: tuple = top_left
        self.br: tuple = bottom_right
        self.rect: rectangle = rectangle(self.tl, self.br)
        self.contents: str = '?'
        self.pot_doses: int(0-4) = 0
