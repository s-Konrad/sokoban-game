from classes import (Agent, Board, InvalidOcupation, InvalidTile,
                     StepableTile, InaccesibleTile, ButtonTile,)
import json


def load_data(fp):
    return json.load(fp)

# class method static methodlevel.py
# class player


def get_board(level_data):
    types_dict = {
        'floor': StepableTile,
        'wall': InaccesibleTile,
        'void': InaccesibleTile,
        'button': ButtonTile,
    }

    tiles = {}
    buttons_ids = []
    level_name = level_data['title']
    tiles_list = level_data['tiles']
    for tile in tiles_list:
        id = tuple(tile['id'])
        type_ = tile['type']
        if id in tiles:
            raise InvalidTile('Tile already exists')

        tiles[id] = types_dict[type_](id)
        if type_ == 'button':
            buttons_ids.append(id)
    board = Board(tiles, buttons_ids)
    return level_name, board


def get_player(level_data):
    player = level_data['player']
    position = tuple(player['position'])
    return Agent(position)

# @TODO sprawdzanie cy jedno nie stoi na drugim(może łączac box i player lub
# agent i dziedziczate box player ktoreych instancje bedza na liscie agent) +
# sprawdzanie czy nie stoja na jednym
# i usunąć id


def get_boxes(level_data) -> dict[Agent]:
    boxes = {}
    boxes_list = level_data['boxes']
    for box in boxes_list:
        id = box['id']
        position = tuple(box['position'])
        if id in boxes:
            raise InvalidOcupation
        boxes[id] = Agent(position)
    return boxes
# gui i sprite https://forum.qt.io/topic/13628/getting-started-with-a-tile
# -based-game-in-qt/2


def get_level(level):
    with open(f'levels/{level}.json') as fp:
        game_data = load_data(fp)
        title, board = get_board(game_data)
        player = get_player(game_data)
        boxes = get_boxes(game_data)
        return title, board, player, boxes
