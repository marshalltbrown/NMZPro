import random


def getTRNV(mean: float, lower: float, upper: float) -> float:
    result = False
    # print(f"Mean: {mean}, Upper = {upper}, lower ={lower}")
    while result < lower or result > upper:
        result = random.normalvariate(mean, (upper-lower) / 4)
    return result


class tab:
    def __init__(self, name: str, top_left: tuple, bottom_right: tuple, f_key=''):
        self.name = name
        self.selected = bool
        self.rect = rectangle(top_left, bottom_right)
        self.f_key = f_key


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
        return ((self.left + self.right) / 2), ((self.top + self.bottom) / 2),

    @property
    def random_coord(self) -> tuple:
        """Returns a normally distributed random coordinate within the rectangle box."""
        mean_x = (self.right + self.left) / 2
        mean_y = (self.top + self.bottom) / 2
        x = getTRNV(mean_x, self.left, self.right)
        y = getTRNV(mean_y, self.top, self.bottom)
        return x, y


class inv_slot:
    def __init__(self, top_left: tuple, bottom_right: tuple):
        self.tl: tuple = top_left
        self.br: tuple = bottom_right
        self.rect: rectangle = rectangle(self.tl, self.br)
        self.contents: str = '?'
