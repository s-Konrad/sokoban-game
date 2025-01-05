from enum import Enum
from classes import Agent, Tile, InaccesibleTile
from classes import StepableTile, ButtonTile, Game, InvalidCoordinates
import pytest


class TestFiles(Enum):
    example = 'test_levels/example.json'
    tile_e = 'test_levels/tile.json'
    player_e = 'test_levels/player.json'
    player_box_e = 'test_levels/player_box.json'
    box_e = 'test_levels/box.json'
    box_box_e = 'test_levels/box_box.json'


def test_tile_valid_coordinates():
    tile = Tile((0, 0))
    assert tile is not None


def test_tile_invalid_coordinates():
    with pytest.raises(InvalidCoordinates):
        Tile((-1, 0))
    with pytest.raises(InvalidCoordinates):
        Tile((0, -1))
    with pytest.raises(InvalidCoordinates):
        Tile((32, 32))


def test_stepable_tile_init():
    tile = StepableTile((1, 1), ocupied=True)
    assert tile is not None
    assert tile._ocupied is True


def test_stepable_tile_can_hold():
    tile = StepableTile((1, 1), ocupied=False)
    assert tile.can_hold() is True


def test_stepable_tile_set_ocupation():
    tile = StepableTile((1, 1), ocupied=False)
    tile.set_ocupation(True)
    assert tile._ocupied is True


def test_button_tile_init():
    button_tile = ButtonTile((2, 2), ocupied=False)
    assert button_tile is not None
    assert button_tile.is_pressed() is False
    button_tile.set_ocupation(True)
    assert button_tile.is_pressed() is True


#  do wywalenia test
def test_inaccesible_tile_init():
    inaccesible_tile = InaccesibleTile((3, 3))
    assert inaccesible_tile is not None


def test_agent_init():
    agent = Agent((0, 0))
    # @TODO out of bounds box player
    assert agent.pos() == (0, 0)


def test_agent_move():
    agent = Agent((0, 0))
    agent.pos() == (0, 0)
    agent.move_right()
    agent.pos() == (1, 0)
    agent.move_left()
    agent.pos() == (0, 0)
    agent.move_up()
    agent.pos() == (0, 1)
    agent.move_down()
    agent.pos() == (0, 0)


def test_game_init():
    player = Agent((0, 0))
    level = ({
        (0, 0): StepableTile((0, 0)),
        (1, 0): StepableTile((1, 0)),
        (0, 1): ButtonTile((0, 1)),
    }, 'Test Level', [(0, 1)])
    boxes = {1: Agent((1, 0))}

    game = Game(player, level, boxes)
    assert game.player.pos() == (0, 0)
    assert str(game.level[(0, 1)]) == 'button'
    assert game.title == "Test Level"
    assert game.moves == 0

#to do player on box
