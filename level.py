from classes import Tile, BoxTile
import csv


d = {
      0: Tile,
      1: BoxTile
}
t = d[0](1, False)
b = d[1](2, False)


def get_level(fp):
    level = []
    reader = csv.DictReader(fp)
    for row in reader:
        position = (row['position_x'], row['position_y'])
        type = row['type']
        tile = Tile(position, type)
        level.append(tile)
    return level
