class InvalidTile(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InvalidAgent(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InaccesibleTileOcupied(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class AgentsOverlaping(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InvalidCoordinates(ValueError):
    def __init__(self, *args):
        super().__init__(*args)


class InaccesibleTile():
    def __init__(self, coordinates: tuple[int, int]) -> None:

        self._location = coordinates

        if not (0 <= coordinates[0] < 16 and 0 <= coordinates[1] < 16):
            raise InvalidCoordinates('Tile cooridnates have to be between '
                                     '0 and 15')

    def __repr__(self) -> str:
        return f'{self._location} - {self.__str__()}'

    def __str__(self) -> str:
        return 'wall'


class StepableTile(InaccesibleTile):
    def __init__(self, coordinates: tuple[int, int]) -> None:
        super().__init__(coordinates)
        self._ocupied = False

    def can_hold(self) -> bool:
        return not self._ocupied

    def set_ocupation(self, is_ocupied: bool) -> None:
        self._ocupied = is_ocupied

    def __str__(self) -> str:
        return 'floor'


class ButtonTile(StepableTile):
    def __init__(self,
                 coordinates: tuple[int, int],
                 ) -> None:
        super().__init__(coordinates)

    def is_pressed(self) -> bool:
        return self._ocupied

    def __str__(self) -> str:
        return 'button'


class Agent():
    def __init__(self, coordinates: tuple[int, int]) -> None:

        if not (0 <= coordinates[0] < 16 and 0 <= coordinates[1] < 16):
            raise InvalidCoordinates('Agent cooridnates have to be between '
                                     '0 and 15')
        self.__location_x, self.__location_y = coordinates

    @property
    def pos(self) -> tuple[int, int]:
        return self.__location_x, self.__location_y

    def move_up(self) -> None:
        self.__location_y += 1

    def move_down(self) -> None:
        self.__location_y -= 1

    def move_left(self) -> None:
        self.__location_x -= 1

    def move_right(self) -> None:
        self.__location_x += 1


class Board():
    def __init__(self,
                 tiles: dict[tuple[int, int]:
                             InaccesibleTile | StepableTile | ButtonTile],
                 buttons: list[tuple[int, int]]
                 ) -> None:
        self._tiles = tiles
        self._buttons = buttons

    @property
    def tiles(self) -> dict[tuple[int, int]:
                            InaccesibleTile | StepableTile | ButtonTile]:
        return self._tiles

    @property
    def buttons(self) -> list[tuple[int, int]]:
        return self._buttons

    def mark_tiles_as_taken(self,
                            boxes: dict[int: Agent]
                            ) -> None:
        for box_id in boxes:
            try:
                self._tiles[boxes[box_id].pos].set_ocupation(True)
            except AttributeError:
                raise InaccesibleTileOcupied('A box is positioned on an'
                                             'inaccesible tile')
            except KeyError:
                raise InvalidCoordinates('Box out of bounds')

    def check_correctness(self,
                          boxes: dict[tuple[int, int]: Agent],
                          player: Agent
                          ) -> None:
        boxes_pos = {boxes[box_id].pos for box_id in boxes}
        if len(boxes_pos) != len(boxes):
            raise AgentsOverlaping('A box is positioned on top of another box')
        try:
            if self._tiles[player.pos].can_hold() is False:
                raise AgentsOverlaping('Player is standing on top of a box')

        except AttributeError:
            raise InaccesibleTileOcupied('Player is on an inaccesible tile')

        except KeyError:
            raise InvalidCoordinates('Player out of bounds')

    def validate_move(self,
                      agent: Agent,
                      move: str
                      ) -> bool:
        x_coords, y_coords = agent.pos
        actions = {
            'w': lambda x, y: (x, y+1),
            'a': lambda x, y: (x-1, y),
            's': lambda x, y: (x, y-1),
            'd': lambda x, y: (x+1, y),
        }
        try:
            future_pos = actions.get(move)(x_coords, y_coords)
        except TypeError:
            return False

        # check if out of bounds
        if future_pos not in self._tiles:
            return False

        # check if tile is accesible and free
        try:
            if self._tiles[future_pos].can_hold():
                return True
        except AttributeError:
            return False

        # above means that there is a box on the future_pos
        # check if player can push it
        x_coords, y_coords = future_pos
        future_pos = actions[move](x_coords, y_coords)
        if future_pos not in self._tiles:
            return False
        try:
            if self._tiles[future_pos].can_hold():
                return True
        except AttributeError:
            return False


class Game():
    def __init__(self,
                 id: int,
                 title: str,
                 board: Board,
                 player: Agent,
                 boxes: dict[int: Agent]
                 ) -> None:
        self.load_level(id, title, board, player, boxes)

    def load_level(self,
                   id: int,
                   title: str,
                   board: Board,
                   player: Agent,
                   boxes: dict[int: Agent]
                   ) -> None:
        self._current_level_id = id
        self._title = title
        self._player = player
        self._board = board
        self._board.mark_tiles_as_taken(boxes)
        self._boxes = boxes
        self._moves = []
        self._board.check_correctness(boxes, player)

    @property
    def player(self) -> Agent:
        return self._player

    @property
    def title(self) -> str:
        return self._title

    @property
    def level_id(self) -> int:
        return self._current_level_id

    def increment_level_id(self) -> None:
        self._current_level_id += 1

# ???
    @property
    def tiles(self) -> dict[tuple[int, int]:
                            InaccesibleTile | StepableTile | ButtonTile]:
        return self._board.tiles

    @property
    def boxes(self) -> dict[int: Agent]:
        return self._boxes

    @property
    def moves_num(self) -> list[tuple[str, tuple[int, int] | None]]:
        return len(self._moves)

    def _find_box(self, coordinates: tuple[int, int]) -> int | None:
        for box_id in self._boxes:
            if self._boxes[box_id].pos == coordinates:
                return box_id
        else:
            return None

    def move(self, move: str) -> None:
        actions = {
            'w': Agent.move_up,
            'a': Agent.move_left,
            's': Agent.move_down,
            'd': Agent.move_right,
        }
        if self._board.validate_move(self._player, move):
            actions[move](self._player)
            box_id = self._find_box(self._player.pos)
            if box_id is None:
                self._moves.append((move, None))
            else:
                box = self._boxes[box_id]
                actions[move](box)
                self._board.tiles[self._player.pos].set_ocupation(False)
                self._board.tiles[box.pos].set_ocupation(True)
                self._moves.append((move, box_id))

    def undo_move(self) -> None:
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
                self._board.tiles[box.pos].set_ocupation(False)
                reverse_action.get(move)(self._boxes[agent])
                self._board.tiles[box.pos].set_ocupation(True)
            self._moves.pop()

    def game_ended(self) -> bool:
        for button_id in self._board.buttons:
            if not self._board.tiles[button_id].is_pressed():
                return False
        else:
            return True
