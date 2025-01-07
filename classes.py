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


class Board():
    def __init__(self,
                 tiles: dict[tuple[int, int]: InaccesibleTile],
                 buttons: list[int, int]
                 ):
        self._tiles = tiles
        self._buttons = buttons

    @property
    def tiles(self):
        return self._tiles

    @property
    def buttons(self):
        return self._buttons

    def mark_tiles(self,
                   boxes: dict[int: Agent]
                   ):
        for box_id in boxes:
            try:
                self._tiles[boxes[box_id].pos()].set_ocupation(True)
            except AttributeError:
                raise InvalidOcupation
            except KeyError:
                raise InvalidCoordinates
        # return self

    def check_correctness(self, boxes, player):
        boxes_pos = {boxes[box_id].pos() for box_id in boxes}
        if len(boxes_pos) != len(boxes):
            raise InvalidOcupation
        try:
            if self._tiles[player.pos()].can_hold() is False:
                raise InvalidOcupation
        except AttributeError:
            raise InvalidOcupation
        except KeyError:
            raise InvalidCoordinates

    def validate_move(self,
                      agent: Agent,
                      move: str
                      ) -> bool:
        x_coords, y_coords = agent.pos()
        actions = {
            'w': lambda x, y: (x, y+1),
            'a': lambda x, y: (x-1, y),
            's': lambda x, y: (x, y-1),
            'd': lambda x, y: (x+1, y),
        }
        sus_pos = actions.get(move)(x_coords, y_coords)
        if not sus_pos:
            return False

        # check if out of bounds
        if sus_pos not in self._tiles:
            return False
        # check if tile is accesible and free
        try:
            if self._tiles[sus_pos].can_hold():
                return True
        except AttributeError:
            return False
            raise InvalidOcupation('InaccesibleTile cannot be taken')
        # above means that there is a box on the sus_pos
        # check if player can push it
        x_coords, y_coords = sus_pos
        sus_pos = actions[move](x_coords, y_coords)
        if sus_pos not in self._tiles:
            return False
        try:
            # niech to nie zwraca pos i niech nie zmienia oc
            if self._tiles[sus_pos].can_hold():
                return True
        except AttributeError:
            return False
            raise InvalidOcupation('InaccesibleTile cannot be taken')


class Game():
    def __init__(self,
                 title: str,
                 board: Board,
                 player: Agent,
                 boxes: dict[int: Agent]
                 ):
        self.load_level(title, board, player, boxes)

    def load_level(self,
                   title: str,
                   board: Board,
                   player: Agent,
                   boxes: dict[int: Agent]
                   ):
        self._title = title
        self._player = player
        # self._level = board.tiles
        # self._buttons = board.buttons
        self._board = board
        self._board.mark_tiles(boxes)
        self._boxes = boxes
        self._moves = []
        self._board.check_correctness(boxes, player)

    @property
    def player(self):
        return self._player

    @property
    def title(self):
        return self._title

# ???
    @property
    def level(self):
        return self._board.tiles

    @property
    def boxes(self):
        return self._boxes

    @property
    def moves(self):
        return len(self._moves)

    def finb_box(self, coordinates):
        for box_id in self._boxes:
            if self._boxes[box_id].pos() == coordinates:
                return box_id
        else:
            return None
            raise IndexError

    def validate_move(self, move):
        self.move(move)
        # if self._board.validate_move(self._player, move):
        #     self.move(move, self._player)
#         try:
#             self._moves.append((move, None))
#             self.move(move, self._player)

#         except KeyError:
#             self.undo_move()
#             return
#         except AttributeError:
#             self.undo_move()
#             return
#         self._board.validate_move(self._player, move)
#         try:
#             box_id = self.finb_box(self.player.pos())
#             box = self._boxes[box_id]
#         except IndexError:
#             return

#         try:
#             self._moves.pop()
#             self._moves.append((move, box_id))
#             self.move(move, box)
#             if not self._board.tiles[box.pos()].can_hold():
#                 self.undo_move()
#                 return
#             # to to zaakomentowan
#             self._board.mark_tiles(self._boxes)
#             # self._level[self.player.pos()].set_ocupation(False)
#             # self._level[box.pos()].set_ocupation(True)
#             return
# # todo jest to except key.... powtorzone 2x wiec moze przniezt to do move albo
# # zamienic funkcjonalnoscia mow do sprawdzanie czy pudełko w validate tylko do
# # except key error...
#         except KeyError:
#             self.undo_move()
#             return
#         except AttributeError:
#             self.undo_move()
#             return

    def move(self, move):
        actions = {
            'w': Agent.move_up,
            'a': Agent.move_left,
            's': Agent.move_down,
            'd': Agent.move_right,
        }
        move_status = self._board.validate_move(self._player, move)
        if move_status:
            actions[move](self._player)
            box_id = self.finb_box(self._player.pos())
            if box_id is None:
                self._moves.append((move, None))
            else:
                box = self._boxes[box_id]
                actions[move](box)
                self._board.tiles[self._player.pos()].set_ocupation(False)
                self._board.tiles[box.pos()].set_ocupation(True)
                self._moves.append((move, box_id))

        # # level = self.level
        # if action:
        #     action(self._player)
        # else:
        #     self._moves.pop()
        #     return

#       ponizej przeneisc do validate
        # tile = level[agent.pos()]
        # tile.can_hold()

# zmienic valid undo na undo move
    def valid_undo(self):
        reverse_action = {
            'w': Agent.move_down,
            'a': Agent.move_right,
            's': Agent.move_up,
            'd': Agent.move_left,
        }
        if len(self._moves) > 0:
            move = self._moves[-1][0]
            agent = self._moves[-1][1]
            reverse_action.get(move)(self._player)
            if agent is not None:
                box = self._boxes[agent]
                self._board.tiles[box.pos()].set_ocupation(False)
                reverse_action.get(move)(self._boxes[agent])
                self._board.tiles[box.pos()].set_ocupation(True)
            self._moves.pop()

    # def valid_undo(self):
    #     try:
    #         agent = self._moves[-1][1]
    #         self.level[self._boxes[agent].pos()].set_ocupation(False)
    #         self.undo_move()
    #         self.level[self._boxes[agent].pos()].set_ocupation(True)
    #     except KeyError:
    #         self.undo_move()
    #     except IndexError:
    #         pass

    def game_ended(self):
        for button_id in self._board.buttons:
            if not self._board.tiles[button_id].is_pressed():
                return False
        else:
            return True
