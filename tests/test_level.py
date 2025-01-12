import pytest
from model import InvalidTile, InvalidAgent
from load_level import (get_title, get_board, get_player, get_boxes,
                        convert_to_int)


def test_convert_to_int():
    assert convert_to_int([1, '1']) == (1, 1)
    with pytest.raises(ValueError):
        convert_to_int([1, 'da'])


SAMPLE_DATA = {
    'title': 'Test Level',
    'tiles': [
        {'id': [0, 0], 'type': 'floor'},
        {'id': [1, 0], 'type': 'wall'},
        {'id': [2, 0], 'type': 'button'}
    ],
    'player_pos': [0, 0],
    'boxes': [
        {'id': 1, 'position': [1, 1]},
        {'id': 2, 'position': [2, 1]}
    ]
}


def test_get_title():
    title = get_title(SAMPLE_DATA)
    assert title == 'Test Level'


def test_get_board():
    board = get_board(SAMPLE_DATA)
    assert len(board.tiles) == 3
    assert board.tiles[(0, 0)].can_hold()
    assert board.tiles[(2, 0)].can_hold()
    assert board.buttons == [(2, 0)]


def test_get_player():
    player = get_player(SAMPLE_DATA)
    assert player.pos == (0, 0)


def test_get_boxes():
    boxes = get_boxes(SAMPLE_DATA)
    assert len(boxes) == 2
    assert boxes[1].pos == (1, 1)
    assert boxes[2].pos == (2, 1)


def test_duplicate_tile():
    duplicate_tile_data = {
        'title': 'Test Level with Duplicate Tiles',
        'tiles': [
            {'id': [0, 0], 'type': 'floor'},
            {'id': [0, 0], 'type': 'wall'}
        ],
        'player_pos': [0, 0],
        'boxes': []
    }

    with pytest.raises(InvalidTile):
        get_board(duplicate_tile_data)


def test_invalid_tile_type():
    duplicate_tile_data = {
        'title': 'Test Level with Duplicate Tiles',
        'tiles': [
            {'id': [0, 0], 'type': 'floor'},
            {'id': [0, 1], 'type': 'unknown'}
        ],
        'player_pos': [0, 0],
        'boxes': []
    }

    with pytest.raises(InvalidTile):
        get_board(duplicate_tile_data)


def test_invalid_tile_location():
    invalid_tile_data = {
        'title': 'Test Level with Duplicate Tiles',
        'tiles': [
            {'id': ['ds', 0], 'type': 'floor'},
            {'id': [0, 1], 'type': 'unknown'}
        ],
        'player_pos': [0, 0],
        'boxes': []
    }

    with pytest.raises(ValueError):
        get_board(invalid_tile_data)


def test_duplicate_box_id():
    duplicate_box_data = {
        'title': 'Test Level with Duplicate Boxes',
        'tiles': [{'id': [0, 0], 'type': 'floor'}],
        'player_pos': [0, 0],
        'boxes': [
            {'id': 1, 'position': [1, 1]},
            {'id': 1, 'position': [2, 1]}
        ]
    }

    with pytest.raises(InvalidAgent):
        get_boxes(duplicate_box_data)


def test_invalid_box_id():
    invalid_box_data = {
        'title': 'Test Level with Duplicate Boxes',
        'tiles': [{'id': [0, 0], 'type': 'floor'}],
        'player_pos': [0, 0],
        'boxes': [
            {'id': 'ds', 'position': [1, 1]},
            {'id': 1, 'position': [2, 1]}
        ]
    }

    with pytest.raises(ValueError):
        get_boxes(invalid_box_data)


def test_invalid_box_pos():
    invalid_box_data = {
        'title': 'Test Level with Duplicate Boxes',
        'tiles': [{'id': [0, 0], 'type': 'floor'}],
        'player_pos': [0, 0],
        'boxes': [
            {'id': 0, 'position': ['$$$', 1]},
            {'id': 1, 'position': [2, 1]}
        ]
    }

    with pytest.raises(ValueError):
        get_boxes(invalid_box_data)


def test_invalid_player_pos():
    invalid_box_data = {
        'title': 'Test Level with Duplicate Boxes',
        'tiles': [{'id': [0, 0], 'type': 'floor'}],
        'player_pos': [0, '$k$'],
        'boxes': [
            {'id': 0, 'position': [1, 1]},
            {'id': 1, 'position': [2, 1]}
        ]
    }

    with pytest.raises(ValueError):
        get_player(invalid_box_data)
