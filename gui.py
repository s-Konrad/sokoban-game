from PySide2.QtWidgets import (QApplication, QMainWindow, QGraphicsScene,
                               QGraphicsSimpleTextItem,)
from PySide2.QtCore import Qt
from ui_sokobon import Ui_MainWindow
from level import get_level, get_boxes, get_players
import sys
import copy


class Gui(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setup_level()
        self.setup_agents()
        self.player_info = get_players()
        self.player_marker = self._scene.addEllipse(-10, -10, 10, 10)
        self.restart_level()

        self.ui.resetButton.clicked.connect(self.restart_level)

    def setup_level(self):

        level, level_name = get_level()
        self._scene = QGraphicsScene()
        self.ui.levelView.setScene(self._scene)
        for tile in level:
            x_coords, y_coords = tile
            marker = self._scene.addRect(-100, -100, 100, 100)
            marker.setPos(x_coords*100, y_coords*-100)
            text_item = QGraphicsSimpleTextItem(str(level[tile]), marker)
            text_item.setPos(-80, -60)

        label = self.ui.levelLabel
        label.setText(level_name)

    def keyPressEvent(self, event):
        action = {
            Qt.Key_R: self.restart_level()
            # Qt.Key_W: pass
        }
        # @TODO ZMIENIĆ PLAYERS NA JEDDNEGO PLAYER
        return super().keyPressEvent(event)

    def setup_agents(self):
        boxes = get_boxes()
        for box in boxes.values():
            x_coords, y_coords = box.pos()
            marker = self._scene.addRect(-10, -10, 10, 10)
            marker.setPos(x_coords*100-50, y_coords*-100-50)

    def draw_players(self, players):
        for player in players.values():
            x_coords, y_coords = player.pos()
            self.player_marker.setPos(x_coords*100, y_coords*-100)

    def restart_level(self):
        self.players = copy.deepcopy(self.player_info)
        self.draw_players(self.players)


def gui_main(args):
    app = QApplication(args)
    window = Gui()
    window.show()
    return app.exec_()


if __name__ == '__main__':

    gui_main(sys.argv)
