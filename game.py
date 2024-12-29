from level import get_floor, get_player, get_boxes
from PySide6.QtCore import Qt

from classes import Agent, Game
from gui import Gui, gui_main


# @TODO przenieść gui i sprawdzanie prezsuwania tutaj
# sprawdzanie try except box in the way
# z classes moveup tu z tad do gui może jako jedno move?


# def move(player, boxes, level, event):
#     action = {
#         Qt.Key_W: Agent.move_up,
#         Qt.Key_S: Agent.move_down,
#         Qt.Key_A: Agent.move_left,
#         Qt.Key_D: Agent.move_right,
#     }
#     action.get(event.key())(player)
#     if player.pos() not in level:
#         undo_move(player, event)
        # print(player.pos())


# usunac te wszystkie przekazywania bo i tak to bedzie wykonywane z poziomu
# game gdy zwine to z gui
def undo_move(player, event):
    pass
    # reverse_action = {
    #     Qt.Key_S: Agent.move_up,
    #     Qt.Key_W: Agent.move_down,
    #     Qt.Key_D: Agent.move_left,
    #     Qt.Key_A: Agent.move_right,
    # }
    # reverse_action.get(event.key())(player)

# def move_up(player, boxes):
#     player.move_up()
#     print(player.pos())
#     for box_id in boxes:
#         if boxes[box_id].pos() == player.pos():
#             boxes[box_id].push_up()
#             print('ns', boxes[box_id].pos())


# zamieniać wywoływanie gui zeby wychodziło z game i zeby level było dostepne
# wtedy ruchy bylyby dostęne do sprawdzania
def game():
    # read tiles placement and its contents from file
    moves = []
    # level, agents = get_floor()

    gui_main()


if __name__ == '__main__':
    game()
