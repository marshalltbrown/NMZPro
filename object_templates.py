class tab:
    def __init__(self, name: str, top_left: tuple, bottom_right: tuple, f_key=''):
        self.name = name
        self.selected = bool
        self.rect = rectangle(top_left, bottom_right)
        self.f_key = f_key


class coord:
    offset: tuple

    def __init__(self, x: int, y: int):
        self.static_x = x
        self.static_y = y

    @property
    def x(self) -> int:
        return self.static_x + coord.offset[0]

    @property
    def y(self) -> int:
        return self.static_y + coord.offset[1]

    @property
    def tuple(self) -> tuple:
        return self.x, self.y,


class rectangle:
    offset: tuple

    def __init__(self, top_left: tuple, bottom_right: tuple):
        self.left_static = top_left[0]
        self.top_static = top_left[1]
        self.right_static = bottom_right[0]
        self.bottom_static = bottom_right[1]

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
    def tl(self):
        return self.left, self.top

    @property
    def br(self):
        return self.right, self.bottom

    @property
    def center(self) -> tuple:
        return ((self.left + self.right) / 2), ((self.top + self.bottom) / 2),


class inv_slot:
    def __init__(self, top_left: tuple, bottom_right: tuple):
        self.tl = top_left
        self.br = bottom_right
        self.rect = rectangle(self.tl, self.br)
        self.contents = '?'
