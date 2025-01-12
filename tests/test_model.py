import pytest
from model import (Agent, InaccesibleTile, StepableTile, ButtonTile, Board,
                   Game, InvalidCoordinates, InaccesibleTileOcupied, AgentsOverlaping)


# Test Tiles
def test_invalid_inaccesible_tile_creation():
    with pytest.raises(InvalidCoordinates):
        InaccesibleTile((16, 16))


def test_valid_inaccesible_tile_creation():
    tile = InaccesibleTile((5, 5))
    assert tile._location == (5, 5)


def test_stepable_tile_creation():
    tile = StepableTile((5, 5))
    assert tile.can_hold() == True


def test_button_tile_creation():
    tile = ButtonTile((5, 5))
    assert tile.is_pressed() == False


# Test Agent
def test_invalid_agent_creation():
    with pytest.raises(InvalidCoordinates):
        Agent((16, 16))


def test_valid_agent_creation():
    agent = Agent((5, 5))
    assert agent.pos == (5, 5)


def test_agent_movement():
    agent = Agent((5, 5))
    agent.move_up()
    assert agent.pos == (5, 6)
    agent.move_left()
    assert agent.pos == (4, 6)


# Test Board
def get_example_board():
    return Board({(0, 0): StepableTile((0, 0)),
                  (0, 1): InaccesibleTile((0, 1)),
                  (1, 0): ButtonTile((1, 0))},
                 [(1, 0)])


def get_straight_board():
    return Board({(0, 0): ButtonTile((0, 0)),
                  (1, 0): StepableTile((1, 0)),
                  (2, 0): StepableTile((2, 0)),
                  (3, 0): InaccesibleTile((3, 0))},
                 [(0, 0)])


def test_board_creation():
    board = get_example_board()
    assert board.tiles[(0, 0)].can_hold()
    assert board.buttons == [(1, 0)]


def test_mark_tiles_valid():
    board = get_example_board()
    assert board.tiles[(0, 0)].can_hold()
    board.mark_tiles_as_taken({0: Agent((0, 0))})
    assert not board.tiles[(0, 0)].can_hold()


def test_mark_tiles_invalid():
    board = get_example_board()
    with pytest.raises(InaccesibleTileOcupied):
        board.mark_tiles_as_taken({0: Agent((0, 1))})
    with pytest.raises(InvalidCoordinates):
        board.mark_tiles_as_taken({0: Agent((0, 2))})


def test_board_correctnes_pass():
    board = get_example_board()
    player = Agent((1, 0))
    boxes = {0: Agent((0, 0))}
    board.check_correctness(boxes, player)


def test_board_correctnes_fail():
    player = Agent((1, 0))
    boxes = {0: Agent((0, 0)), 1: Agent((0, 0))}
    with pytest.raises(AgentsOverlaping):
        board = get_example_board()
        board.mark_tiles_as_taken(boxes)
        board.check_correctness(boxes, player)

    boxes = {0: Agent((1, 0))}
    with pytest.raises(AgentsOverlaping):
        board = get_example_board()
        board.mark_tiles_as_taken(boxes)
        board.check_correctness(boxes, player)

    player = Agent((0, 1))
    with pytest.raises(InaccesibleTileOcupied):
        board.check_correctness(boxes, player)

    player = Agent((0, 2))
    with pytest.raises(InvalidCoordinates):
        board.check_correctness(boxes, player)


def test_validate_move():
    player = Agent((0, 0))
    boxes = {}
    board = get_example_board()
    board.mark_tiles_as_taken(boxes)
    assert board.validate_move(player, 'd')
    assert not board.validate_move(player, 's')
    assert not board.validate_move(player, 'w')


def test_complex_validate_move():
    player = Agent((0, 0))
    boxes = {0: Agent((1, 0))}
    board = get_straight_board()
    board.mark_tiles_as_taken(boxes)
    assert board.validate_move(player, 'd')

    player = Agent((1, 0))
    boxes = {0: Agent((2, 0))}
    board = get_straight_board()
    board.mark_tiles_as_taken(boxes)
    assert not board.validate_move(player, 'd')

    boxes = {0: Agent((1, 0)), 1: Agent((2, 0))}
    board = get_straight_board()
    board.mark_tiles_as_taken(boxes)
    assert not board.validate_move(player, 'd')


# Test Game
def test_load_level():
    id = 0
    title = 'example'
    board = get_example_board()
    player = Agent((0, 0))
    boxes = {0: Agent((1, 0))}
    game = Game(id, title, board, player, boxes)

    assert game.moves_num == 0
    assert game.tiles == board.tiles
    assert game.player == player
    assert game.title == title
    assert game.level_id == id
    assert game.boxes == boxes


def test_find_box():
    id = 0
    title = 'example'
    board = get_example_board()
    player = Agent((0, 0))
    boxes = {0: Agent((1, 0))}
    game = Game(id, title, board, player, boxes)

    assert game._find_box((1, 0)) == 0


def test_move_valid():
    id = 0
    title = 'example'
    board = get_example_board()
    player = Agent((0, 0))
    boxes = {}
    game = Game(id, title, board, player, boxes)

    game.move('d')
    assert game.moves_num == 1
    assert player.pos == (1, 0)


def test_move_invalid():
    id = 0
    title = 'example'
    board = get_example_board()
    player = Agent((0, 0))
    boxes = {0: Agent((1, 0))}
    game = Game(id, title, board, player, boxes)

    game.move('d')
    assert player.pos == (0, 0)


def test_push_box():
    id = 0
    title = 'example'
    board = get_straight_board()
    player = Agent((0, 0))
    boxes = {0: Agent((1, 0))}
    game = Game(id, title, board, player, boxes)

    box = boxes[0]
    assert not board.tiles[(1, 0)].can_hold()
    assert player.pos == (0, 0)
    assert box.pos == (1, 0)
    game.move('d')
    assert player.pos == (1, 0)
    assert board.tiles[(1, 0)].can_hold()
    assert box.pos == (2, 0)
    assert not board.tiles[(2, 0)].can_hold()


def test_unable_to_push_box():
    id = 0
    title = 'example'
    board = get_straight_board()
    player = Agent((1, 0))
    boxes = {0: Agent((2, 0))}
    game = Game(id, title, board, player, boxes)

    box = boxes[0]
    assert player.pos == (1, 0)
    assert box.pos == (2, 0)
    game.move('d')
    assert player.pos == (1, 0)
    assert box.pos == (2, 0)


def test_undo_move():
    id = 0
    title = 'example'
    board = get_example_board()
    player = Agent((0, 0))
    boxes = {}
    game = Game(id, title, board, player, boxes)

    game.move('d')
    assert game.moves_num == 1
    assert player.pos == (1, 0)
    game.undo_move()
    assert game.moves_num == 0
    assert player.pos == (0, 0)


def test_game_end_condition():
    id = 0
    title = 'example'
    board = Board({(0, 0): StepableTile((0, 0)),
                   (1, 0): StepableTile((1, 0)),
                   (2, 0): StepableTile((2, 0)),
                   (3, 0): ButtonTile((3, 0))},
                  [(3, 0)])
    player = Agent((1, 0))
    boxes = {0: Agent((2, 0))}
    game = Game(id, title, board, player, boxes)

    assert not game.game_ended()
    game.move('d')
    assert game.game_ended()
