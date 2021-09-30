class tab:  # TODO: Finish implementing proper tab objects for code clarity
    def __init__(self, name: str, top_left: tuple, bottom_right: tuple, f_key=''):
        self.name = name
        self.selected = bool
        self.rect = rectangle(top_left, bottom_right)
        self.f_key = f_key

    def set_offset(self, offset) -> None:
        self.rect.set_rect(offset)


class coord:
    def __init__(self, x: int, y: int):
        self.static_x = x
        self.static_y = y
        self.x = int
        self.y = int
        self.tuple = tuple

    def set_offset(self, offset: tuple) -> None:
        self.x = self.static_x + offset[0]
        self.y = self.static_y + offset[1]
        self.tuple = (self.x, self.y,)


class rectangle:
    def __init__(self, top_left: tuple, bottom_right: tuple):
        self.left_static = top_left[0]
        self.top_static = top_left[1]
        self.right_static = bottom_right[0]
        self.bottom_static = bottom_right[1]
        self.left = int
        self.top = int
        self.right = int
        self.bottom = int
        self.center = tuple

    def set_rect(self, offset: tuple) -> None:
        self.left = self.left_static + offset[0]
        self.top = self.top_static + offset[1]
        self.right = self.right_static + offset[0]
        self.bottom = self.bottom_static + offset[1]
        self.center = (((self.left + self.right) / 2), ((self.top + self.bottom) / 2),)


class inv_slot:
    def __init__(self, top_left: tuple, bottom_right: tuple):
        self.tl = top_left
        self.br = bottom_right
        self.rect = rectangle(self.tl, self.br)
        self.contents = '?'

    def set_offset(self, offset: tuple) -> None:
        self.rect.set_rect(offset)
