class InvalidTile(Exception):
    pass


class OcupationError(Exception):
    pass


# @dataclass
class Tile():
    '''
    type:
    0 void
    1 wall
    2 floor
    3 button
    # 4 box spawn inherit tile_stepable tile(tile), Inaccesive_tile
    # 5 player spawn to na @TODO no spawn tiles only floro
    jak najmniej if można też zrobić inaccesibleTile po prostu w tile skoro i 
    tak nic nie robi
    '''
    def __init__(self,
                 coordinates,
                 tile_type='void',) -> None:

        self.__location = coordinates
        try:
            self.__type = tile_type
        except Exception:
            raise Exception

        if not (0 <= coordinates[0] < 32 and 0 <= coordinates[1] < 32):
            raise ValueError

        # if tile_type in [0, 1]:
        #     if ocupied is not None:
        #         raise InvalidTile
        # elif ocupied not in [True, False]:
        #     raise InvalidTile

    def __str__(self):
        return 'unknown'


class StepableTile(Tile):
    def __init__(self, coordinates, tile_type='floor', ocupied=None):
        super().__init__(coordinates, tile_type)
        self.__ocupied = ocupied

    def set_ocupation(self, oc):
        # if?
        self.__ocupied = oc
    
    def __str__(self):
        return 'floor'


class ButtonTile(StepableTile):
    def __init__(self, coordinates, tile_type='button', ocupied=None):
        super().__init__(coordinates, tile_type, ocupied)
        self._ocupied = ocupied

    def is_pressed(self):
        return self._ocupied == 'box'

    def __str__(self):
        return 'button'


class InaccesibleTile(Tile):
    def __init__(self, coordinates, tile_type='void'):
        super().__init__(coordinates, tile_type)

# class WallTile(Tile):
#     def __init__(self, coordinates, has_box=None):
#         super().__init__(coordinates, has_box=None)


# class FloorTile(Tile):
#     def __init__(self, coordinates, has_box=None):
#         super().__init__(coordinates, has_box=None)


#     def is_taken(self):
#         return self.__has_box


# class ButtonTile(Tile):
#     def __init__(self, coordinates, has_box=None):
#         super().__init__(coordinates, has_box=False)
class Player():
    def __init__(self, coordinates):
        self.__location_x, self.__location_y = coordinates
#  z zewnątrz sprawdzanie czy jest możliwość ruchu

    def pos(self):
        return (self.__location_x, self.__location_y)

    def move_up(self):
        self.__location_y += 1

    def move_down(self):
        self.__location_y -= 1

    def move_left(self):
        self.__location_x -= 1

    def move_right(self):
        self.__location_x += 1


class Box():
    def __init__(self, coordinates):
        self.__location_x, self.__location_y = coordinates

    def pos(self):
        return (self.__location_x, self.__location_y)

    def push_up(self):
        pass

    def push_down(self):
        pass

    def push_left(self):
        pass

    def push_right(self):
        pass
