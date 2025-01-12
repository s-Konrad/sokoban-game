from model import (Agent, Board, InvalidTile,
                   StepableTile, InaccesibleTile, ButtonTile, InvalidAgent)
import json


def convert_to_int(data):
    output_list = []
    for element in data:
        output_list.append(int(element))
    return tuple(output_list)


def load_data(fp) -> dict:
    return json.load(fp)


def get_title(level_data: dict) -> str:
    return level_data['title']


def get_board(level_data: dict) -> tuple[str, Board]:
    types_dict = {
        'floor': StepableTile,
        'wall': InaccesibleTile,
        'button': ButtonTile,
    }

    tiles = {}
    buttons_ids = []
    tiles_list = level_data['tiles']
    for tile in tiles_list:
        id = convert_to_int(tile['id'])
        type_ = tile['type']
        if id in tiles:
            raise InvalidTile('Tile already exists')
        if type_ not in types_dict:
            raise InvalidTile('Incorrect tile type')
        tiles[id] = types_dict[type_](id)
        if type_ == 'button':
            buttons_ids.append(id)
    board = Board(tiles, buttons_ids)
    return board


def get_player(level_data: dict) -> Agent:
    position = convert_to_int(level_data['player_pos'])
    return Agent(position)


def get_boxes(level_data: dict) -> dict[Agent]:
    boxes = {}
    boxes_list = level_data['boxes']
    for box in boxes_list:
        id = int(box['id'])
        position = convert_to_int(box['position'])
        if id in boxes:
            raise InvalidAgent('Box with this id already exists')
        boxes[id] = Agent(position)
    return boxes


def get_level(level_id: int) -> tuple[str,
                                      Board,
                                      Agent,
                                      dict[tuple[int, int]: Agent]]:
    with open(f'levels/{level_id}.json') as fp:
        game_data = load_data(fp)
        title = get_title(game_data)
        board = get_board(game_data)
        player = get_player(game_data)
        boxes = get_boxes(game_data)
        return title, board, player, boxes
