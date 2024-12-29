from PySide6.QtWidgets import (QApplication, QStackedWidget, QGraphicsScene,
                               QGraphicsSimpleTextItem, QWidget, QMainWindow)
from ui_sokobon import Ui_gameWindow
from ui_menu import Ui_Form
from ui_pass_screen import Ui_PassWindow
from PySide6.QtCore import Qt
from classes import Game
# from game import move
# z classes import game
from level import get_level
import sys


class Gui(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


class GameWindow(QWidget):
    def __init__(self, game, parent=None, stack=None):
        super().__init__(parent)
        self.ui = Ui_gameWindow()
        self.ui.setupUi(self)
        self.stack = stack
# połACZyc box i player w agents do resetu i do self boxes
        self._scene = QGraphicsScene()
        self._game_instance = game
        # usunac ponizsze przypisania
        self.level, self.level_name = game.level, game.title
        self.player_info = game.player
        self.boxes = self._game_instance.boxes
        # self.setup_tiles()
        self.box_markers = {}
        self.setup_level()
        # self.setup_boxes()
        self.restart_level()
        # self.box_markers

        self.ui.resetButton.clicked.connect(self.restart_level)

    def setup_level(self):
        self.setup_tiles()
        self.player_marker = self._scene.addEllipse(-10, -10, 10, 10)
        self.setup_boxes()

    def setup_tiles(self):
        # level w self
        self._scene.clear()
        self.ui.levelView.setScene(self._scene)
        level = self._game_instance.level
        for tile in level:
            x_coords, y_coords = tile
            marker = self._scene.addRect(-100, -100, 100, 100)
            marker.setPos(x_coords*100, y_coords*-100)
            text_item = QGraphicsSimpleTextItem(str(level[tile]), marker)
            text_item.setPos(-80, -60)

        label = self.ui.levelLabel
        label.setText(self._game_instance.title)
        move_counter = self.ui.moveCounter
        move_counter.setText(f'Moves: {self._game_instance.moves}')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.restart_level()
        elif event.key() == Qt.Key_U:
            self._game_instance.undo_move()
        else:

            self._game_instance.validate_move(event.text())

        self.draw_agents()
        if self._game_instance.game_ended():
            self.stack.setCurrentIndex(2)
            # self.moveCounter.setText(str(self._game_instance.moves))
        move_counter = self.ui.moveCounter
        move_counter.setText(f'Moves: {self._game_instance.moves}')
        return super().keyPressEvent(event)

    def setup_boxes(self):
        for box_id in self._game_instance.boxes:
            x_coords, y_coords = self.boxes[box_id].pos()
            marker = self._scene.addRect(-10, -10, 10, 10)
            marker.setPos(x_coords*100-50, y_coords*-100-50)
            self.box_markers[box_id] = marker

    def draw_agents(self):
        x_coords, y_coords = self._game_instance.player.pos()
        self.player_marker.setPos(x_coords*100, y_coords*-100)
        for box_id in self._game_instance.boxes:
            x_coords, y_coords = self._game_instance.boxes[box_id].pos()
            self.box_markers[box_id].setPos(x_coords*100-50, y_coords*-100-50)

    def restart_level(self, level=None):
        # @TODO zmienic kkopie fasf uprzatnac przekazywanie danych z game do gui pls
        self._game_instance.load_level(*get_level(1))
        move_counter = self.ui.moveCounter
        move_counter.setText(f'Moves: {self._game_instance.moves}')

        self.draw_agents()


class Menu(QWidget):
    def __init__(self, parent=None, stack=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.stack = stack
        self.ui.PlayButton.clicked.connect(self.play)

    def play(self):
        # self.hide()
        self.stack.setCurrentIndex(1)


class PassScreen(QWidget):
    def __init__(self, game, parent=None, stack=None):
        super().__init__(parent)
        self.ui = Ui_PassWindow()
        self.pc = 1
        self.ui.setupUi(self)
        self.stack = stack
        self.parent_ = parent
        self.game = game
        # self.ui.nextLevelButton.clicked.connect(self.go_to_level)
        self.ui.moveCounter.setText(str(self.parent_._game_instance.moves))

    def show(self):
        self.ui.moveCounter.setText(str(self.game.moves))
        return super().show()

    def go_to_level(self):
        try:
            self.pc += 1
            self.game.load_level(*get_level(self.pc))
            self.parent_.setup_level()
            # self.parent_.setup_tiles()
            # self.parent_.setup_boxes()
            self.parent_.draw_agents()
            self.stack.setCurrentIndex(1)
        except FileNotFoundError:
            self.ui.label_2.setText('Awesome! You passed the game')
            self.ui.nextLevelButton.hide()
            self.ui.moveCounter.hide()


def gui_main(argv):
    app = QApplication(argv)
    game = Game(*get_level(1))
    stack = QStackedWidget()
    menu_window = Menu()
    game_window = GameWindow(game)
    pass_window = PassScreen(game, game_window)

    stack.addWidget(menu_window)
    stack.addWidget(game_window)
    stack.addWidget(pass_window)
    menu_window.stack = stack
    game_window.stack = stack
    pass_window.stack = stack
    stack.show()
    pass_window.ui.nextLevelButton.clicked.connect(pass_window.go_to_level)

    # game_window.show()
    # menu_window.show()
    return app.exec()


if __name__ == '__main__':

    gui_main(sys.argv)
