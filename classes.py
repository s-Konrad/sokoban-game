class InvalidTile(Exception):
    pass


class InvalidOcupation(Exception):
    pass
# zamienic na overlapingAgents i Not stepable


class InvalidCoordinates(ValueError):
    pass


# @dataclass
class InaccesibleTile():
    def __init__(self, coordinates) -> None:

        self.__location = coordinates

        if not (0 <= coordinates[0] < 16 and 0 <= coordinates[1] < 16):
            raise InvalidCoordinates

# brush marker here?
    def __str__(self) -> str:
        return 'wall'


class StepableTile(InaccesibleTile):
    def __init__(self, coordinates, ocupied=False) -> None:
        super().__init__(coordinates)
        self._ocupied = ocupied

    def can_hold(self) -> bool:
        return not self._ocupied

    def set_ocupation(self, oc) -> None:
        self._ocupied = oc
# str -> repr loc + type

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


class Agent():
    def __init__(self, coordinates):

        if not (0 <= coordinates[0] < 16 and 0 <= coordinates[1] < 16):
            raise InvalidCoordinates
        self.__location_x, self.__location_y = coordinates

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
        self._check_correctness()

    def _check_correctness(self):
        boxes_pos = {self._boxes[box_id].pos() for box_id in self._boxes}
        if len(boxes_pos) != len(self._boxes):
            raise InvalidOcupation
        try:
            if self._level[self._player.pos()].can_hold() is False:
                raise InvalidOcupation
        except AttributeError:
            raise InvalidOcupation
        except KeyError:
            raise InvalidCoordinates

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
            try:
                self._level[self._boxes[box_id].pos()].set_ocupation(True)
            except AttributeError:
                raise InvalidOcupation
            except KeyError:
                raise InvalidCoordinates

    def finb_box(self, coordinates):
        for box_id in self._boxes:
            if self._boxes[box_id].pos() == coordinates:
                return box_id
        else:
            raise IndexError

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
        except IndexError:
            return

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
# todo jest to except key.... powtorzone 2x wiec moze przniezt to do move albo
# zamienic funkcjonalnoscia mow do sprawdzanie czy pudełko w validate tylko do
# except key error...
        except KeyError:
            self.undo_move()
            return
        except AttributeError:
            self.undo_move()
            return

    def move(self, move, agent):
        actions = {
            'w': Agent.move_up,
            'a': Agent.move_left,
            's': Agent.move_down,
            'd': Agent.move_right,
        }
        action = actions.get(move)
        level = self.level
        if action:
            action(agent)
        else:
            self._moves.pop()
            return

#       ponizej przeneisc do validate
        tile = level[agent.pos()]
        tile.can_hold()

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
        except IndexError:
            pass

    def game_ended(self):
        for button_id in self._buttons:
            if not self._level[button_id].is_pressed():
                return False
        else:
            return True
