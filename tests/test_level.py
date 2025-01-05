from level import get_boxes, get_floor, get_player, load_data
from classes import Agent, InvalidOcupation, InvalidTile
import pytest
from tests.test_classes import TestFiles


def test_get_player():
    with open(TestFiles.example.value) as fp:
        data = load_data(fp)
        get_player(data) == Agent((0, 0))


def test_get_floor():
    with open(TestFiles.example.value) as fp:
        data = load_data(fp)
        tiles, name, button_ids = get_floor(data)
        assert len(tiles) == 7
        assert name == 'Level 1'
        assert len(button_ids) == 1

    with open(TestFiles.tile_e.value) as fp:
        data = load_data(fp)
        with pytest.raises(InvalidTile):
            len(get_floor(data))


def test_get_box():
    with open(TestFiles.example.value) as fp:
        data = load_data(fp)
        get_boxes(data) == {0: Agent((0, 1))}

    with open(TestFiles.box_e.value) as fp:
        data = load_data(fp)
        with pytest.raises(InvalidOcupation):
            get_boxes(data)
