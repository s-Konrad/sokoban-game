from level import get_level, get_player, get_boxes
from PySide6.QtCore import Qt
import copy
from classes import Player
# from gui import Gui, gui_main

def render(level, agents):
    p = 0
    s = ''
    for tile in level:
        if tile[1] == p:
            s += str(level[tile])
        else:
            p += 1
            print(s)
            s = str(level[tile])
    print(s)
    # for agent in agents:
        # print(agent, ' - ', agents[agent].pos())
# @TODO przenieść gui i sprawdzanie prezsuwania tutaj
# sprawdzanie try except box in the way
# z classes moveup tu z tad do gui może jako jedno move?


def move(player, boxes, level, event):
    action = {
        Qt.Key_W: Player.move_up,
        Qt.Key_S: Player.move_down,
        Qt.Key_A: Player.move_left,
        Qt.Key_D: Player.move_right,
    }
    action.get(event.key())(player)
    if player.pos() not in level:
        undo_move(player, event)
        # print(player.pos())


# usunac te wszystkie przekazywania bo i tak to bedzie wykonywane z poziomu game gdy zwine to z gui
def undo_move(player, event):
    reverse_action = {
        Qt.Key_S: Player.move_up,
        Qt.Key_W: Player.move_down,
        Qt.Key_D: Player.move_left,
        Qt.Key_A: Player.move_right,
    }
    reverse_action.get(event.key())(player)

# def move_up(player, boxes):
#     player.move_up()
#     print(player.pos())
#     for box_id in boxes:
#         if boxes[box_id].pos() == player.pos():
#             boxes[box_id].push_up()
#             print('ns', boxes[box_id].pos())


# def move_down(player, boxes):
#     try:
#         player.move_down()
#         print(player.pos())
#     except boxes[player.pos()]:
#         boxes[player.pos()].push_down()


# def move_left(player, boxes):
#     try:
#         player.move_left()
#         print(player.pos())
#     except boxes[player.pos()]:
#         boxes[player.pos()].push_left()


# przeniesc player i box do jednej klasy z move
# def move_right(player, boxes):
#     try:
#         player.move_right()
#         # print(player.pos())
#     except boxes[player.pos()]:
#         boxes[player.pos()].push_right()


# zamieniać wywoływanie gui zeby wychodziło z game i zeby level było dostepne
# wtedy ruchy bylyby dostęne do sprawdzania
def game():
    # read tiles placement and its contents from file
    moves = []
    level, agents = get_level()
    render(level, agents)
    # gui_main()


if __name__ == '__main__':
    game()
