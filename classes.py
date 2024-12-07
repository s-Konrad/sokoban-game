
class Tile():
    def __init__(self, coordinates, has_box=False, is_wall=False,
                 can_hold=False):
        self.__has_box = has_box
        self.__is_wall = is_wall
        self.__can_hold = can_hold
        self.__location = coordinates
