
class Tile():
    def __init__(self, coordinates, has_box=False, is_wall=False,
                 can_hold=False, is_empty=True):
        self.__has_box = has_box
        self.__is_wall = is_wall
        self.__can_hold = can_hold
        self.__location = coordinates
        self.__is_empty = False


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
    def __init__(self, coordinates, has_box=False, is_wall=False,
                 can_hold=False, is_empty=True):
        super().__init__(coordinates, has_box, is_wall, can_hold, is_empty)
