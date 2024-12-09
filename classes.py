
class Tile():
    def __init__(self, coordinates, is_empty=True):
        self.__location = coordinates
        self.__is_empty = is_empty


class Player():
    def __init__(self, coordinates):
        self.__location = coordinates

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass


class BoxTile(Tile):
    def __init__(self, coordinates, is_empty=True):
        super().__init__(coordinates, is_empty)

    def push_up(self):
        pass

    def push_down(self):
        pass

    def push_left(self):
        pass

    def push_right(self):
        pass
