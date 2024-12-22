from PySide2.QtWidgets import (QApplication, QMainWindow, QGraphicsScene,
                               QGraphicsSimpleTextItem)
from ui_sokobon import Ui_MainWindow
from level import get_level, load_data
import sys


class Gui(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        with open('example.json') as fp:
            data = load_data(fp)
        self.setup_level(data)

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


def gui_main(args):
    app = QApplication(args)
    window = Gui()
    window.show()
    return app.exec_()


if __name__ == '__main__':

    gui_main(sys.argv)
