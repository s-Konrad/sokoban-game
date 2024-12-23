from PySide2.QtWidgets import (QApplication, QMainWindow, QGraphicsScene,
                               QGraphicsSimpleTextItem,)
from ui_sokobon import Ui_MainWindow
from level import get_level, load_data, get_boxes, get_players
import sys


class Gui(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        with open('example.json') as fp:
            data = load_data(fp)
        self.setup_level(data)
        self.marker = self._scene.addEllipse(-10, -10, 10, 10)
        players = get_players(data)
        self.draw_players(players)
        self.setup_agents(data)

    def setup_level(self, load_data):

        level = get_level(load_data)
        self._scene = QGraphicsScene()
        self.ui.levelView.setScene(self._scene)
        for tile in level:
            x_coords, y_coords = tile
            marker = self._scene.addRect(-100, -100, 100, 100)
            marker.setPos(x_coords*100, y_coords*-100)
            text_item = QGraphicsSimpleTextItem(str(level[tile]), marker)
            text_item.setPos(-80, -60)

        label = self.ui.levelLabel
        label.setText(load_data['title'])

    def setup_agents(self, load_data):
        boxes = get_boxes(load_data)
        for box in boxes.values():
            x_coords, y_coords = box.pos()
            marker = self._scene.addRect(-10, -10, 10, 10)
            marker.setPos(x_coords*100, y_coords*-100)

    def draw_players(self, players):
        for player in players.values():
            x_coords, y_coords = player.pos()
            self.marker.setPos(x_coords*100, y_coords*-100)

        def set_label():
            for player in players.values():
                player.move_left()
            self.draw_players(players)
            print(f'{players}\n')
# for some reason clicked happens multiple times at once may be a recursion problem
        self.ui.resetButton.clicked.connect(set_label)


def gui_main(args):
    app = QApplication(args)
    window = Gui()
    window.show()
    return app.exec_()


if __name__ == '__main__':

    gui_main(sys.argv)
