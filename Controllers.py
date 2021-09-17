

class admin:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            print(f"K: {key}, V: {value}")
            setattr(self, key, value)

        for key, value in self.__dict__:
            print(f"K: {key}, V: {value}")