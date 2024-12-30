class InvalidTile(Exception):
    pass


class OcupationError(Exception):
    pass


class UnableToHold(Exception):
    pass


class InvalidCoordinates(ValueError):
    pass


class HasBox(Exception):
    pass


class NotStepable(Exception):
    pass

from time import sleep

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
    tak nic nie robi zrobic przesuwanie z try
    '''
    def __init__(self, coordinates) -> None:

        self.__location = coordinates

        if not (0 <= coordinates[0] < 32 and 0 <= coordinates[1] < 32):
            raise InvalidCoordinates

    def is_stepable(self):
        return False
        # if tile_type in [0, 1]:
        #     if ocupied is not None:
        #         raise InvalidTile
        # elif ocupied not in [True, False]:
        #     raise InvalidTile

    def __str__(self):
        return 'unknown'


class StepableTile(Tile):
    def __init__(self, coordinates, ocupied=False):
        super().__init__(coordinates)
        self._ocupied = ocupied

# negate stepable from notStepable Class
    def can_hold(self):
        return not self._ocupied

    def set_ocupation(self, oc):
        # if?
        self._ocupied = oc

    def __str__(self):
        return 'floor'


class ButtonTile(StepableTile):
    def __init__(self, coordinates, ocupied=False):
        super().__init__(coordinates, ocupied)
        self._ocupied = ocupied

    def is_pressed(self):
        return self._ocupied

    def __str__(self):
        return 'button'


class InaccesibleTile(Tile):
    def __init__(self, coordinates):
        super().__init__(coordinates)


# class WallTile(Tile): ->> inaccesibleTile
# odpowiednie metody i hierarchia

class Agent():
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


class Game():
    def __init__(self, player, level, boxes):
        self.load_level(player, level, boxes)

    def load_level(self, player, level, boxes):
        self._player = player
        self._level, self._title, self._buttons = level
        self._boxes = boxes
        self._moves = []
        self.mark_tiles()

    @property
    def player(self):
        return self._player

    @property
    def title(self):
        return self._title

    @property
    def level(self):
        return self._level

    @property
    def boxes(self):
        return self._boxes

    @property
    def moves(self):
        return len(self._moves)

    def mark_tiles(self):
        for box_id in self._boxes:
            self._level[self._boxes[box_id].pos()].set_ocupation(True)

    def finb_box(self, coordinates):
        for box_id in self._boxes:
            if self._boxes[box_id].pos() == coordinates:
                return box_id
        else:
            raise IndexError
    # rozdzielic move na wykonywanie ruchu i sprawdzanie warunku.

    def validate_move(self, move):
        try:
            self._moves.append((move, None))
            self.move(move, self._player)

        except KeyError:
            self.undo_move()
            return
        except AttributeError:
            self.undo_move()
            return
        try:
            box_id = self.finb_box(self.player.pos())
            box = self._boxes[box_id]
            try:
                self._moves.pop()
                self._moves.append((move, box_id))
                self.move(move, box)
                if not self._level[box.pos()].can_hold():
                    self.undo_move()
                    return

                self._level[self.player.pos()].set_ocupation(False)
                self._level[box.pos()].set_ocupation(True)
                return

                # print(box.pos())
            except KeyError:
                self.undo_move()
                return
            except AttributeError:
                self.undo_move()
                return
        except IndexError:
            pass

    def move(self, move, agent):
        actions = {
            'w': Agent.move_up,
            'a': Agent.move_left,
            's': Agent.move_down,
            'd': Agent.move_right,
        }
        action = actions.get(move)
        # player = self.player
        level = self.level
        if action:
            action(agent)
        else:
            self._moves.pop()
            return

        tile = level[agent.pos()]
        tile.can_hold()
        # try:
        #     box = self.finb_box(player.pos())
        #     try:
        #         action(box)
        #     except Ellipsis:
        #         pass
        #     # self.undo_move()
        # except IndexError:
        #     pass


        # zamienić to gorne na sprawdzanie wywolania tile.is stepable
        # for box_id in self._boxes:
        #     if self._boxes[box_id].pos() == self._player.pos():
        #         action.get(move)(self._boxes[box_id])
        #         if
        #         break

    def undo_move(self):
        reverse_action = {
            'w': Agent.move_down,
            'a': Agent.move_right,
            's': Agent.move_up,
            'd': Agent.move_left,
        }
        move = self._moves[-1][0]
        agent = self._moves[-1][1]
        reverse_action.get(move)(self._player)
        if agent is not None:
            reverse_action.get(move)(self._boxes[agent])
        self._moves.pop()

    def valid_undo(self):
        try:
            agent = self._moves[-1][1]
            self._level[self._boxes[agent].pos()].set_ocupation(False)
            self.undo_move()
            self._level[self._boxes[agent].pos()].set_ocupation(True)
        except KeyError:
            self.undo_move()

# zmienic values na liste
    def game_ended(self):
        for button_id in self._buttons:
            if not self._level[button_id].is_pressed():
                return False
        else:
            return True

