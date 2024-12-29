from PySide6.QtWidgets import (QApplication, QStackedWidget, QGraphicsScene,
                               QGraphicsSimpleTextItem, QWidget, QMainWindow)
from ui_sokobon import Ui_gameWindow
from ui_menu import Ui_Form
from ui_pass_screen import Ui_PassWindow
from ui_gui import Ui_MainWindow
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QTimer
from classes import Game
# from game import move
# z classes import game
from level import get_level
import sys


class Gui(QMainWindow):
    def __init__(self, menu, game_window, pass_window, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.addWidget(menu)
        self.ui.stackedWidget.addWidget(game_window)
        self.ui.stackedWidget.addWidget(pass_window)
        self.pass_window = pass_window
        self.menu = menu
        self.game_window = game_window
        self.menu.ui.PlayButton.clicked.connect(self.go_to_game)
        self.pass_window.ui.nextLevelButton.clicked.connect(self.go_to_level)

        self.pc = 1

    def go_to_game(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def go_to_level(self):

        try:
            self.pc += 1
            self.pass_window.ui.moveCounter.setText(str(self.game_window._game_instance.moves))
            self.game_window._game_instance.load_level(*get_level(self.pc))
            self.game_window.setup_level()
            self.game_window.draw_agents()
            self.ui.stackedWidget.setCurrentIndex(1)
        except FileNotFoundError:
            self.ui.stackedWidget.setCurrentIndex(2)
            end_screen = self.pass_window.ui
            end_screen.label_2.setText('Awesome! You passed the game')
            end_screen.ui.nextLevelButton.hide()
            end_screen.ui.moveCounter.hide()


class GameWindow(QWidget):
    def __init__(self, game, parent=None):
        super().__init__(parent)
        self.ui = Ui_gameWindow()
        self.ui.setupUi(self)
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
        self.player_marker = self._scene.addEllipse(-30, -30, 30, 30)
        self.player_marker.setBrush(QColor("#0000ff"))
        self.setup_boxes()

    def setup_tiles(self):
        # level w self
        self._scene.clear()
        self.ui.levelView.setScene(self._scene)
        level = self._game_instance.level
        for tile_id in level:
            x_coords, y_coords = tile_id
            marker = self._scene.addRect(-100, -100, 100, 100)
            marker.setPos(x_coords*100, y_coords*-100)
            marker.setBrush(QColor("#eeeeee"))
            if str(level[tile_id]) == 'unknown':
                marker.setBrush(QColor("#444444"))
            elif str(level[tile_id]) == 'button':
                marker = self._scene.addRect(-70, -70, 70, 70)
                marker.setPos(x_coords*100-15, y_coords*-100-15)
                marker.setBrush(QColor("#ff0000"))

            # text_item = QGraphicsSimpleTextItem(str(level[tile_id]), marker)
            # text_item.setPos(-80, -60)

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
            self.parent().widget(2).ui.moveCounter.setText(f'{self._game_instance.moves} moves')
            QTimer.singleShot(400, lambda: self.parent().setCurrentIndex(2))
            # sleep(2)
            # self.moveCounter.setText(str(self._game_instance.moves))
        move_counter = self.ui.moveCounter
        move_counter.setText(f'Moves: {self._game_instance.moves}')
        return super().keyPressEvent(event)

    def setup_boxes(self):
        for box_id in self._game_instance.boxes:
            x_coords, y_coords = self._game_instance.boxes[box_id].pos()
            marker = self._scene.addRect(-30, -30, 30, 30)
            marker.setPos(x_coords*100-50, y_coords*-100-50)
            marker.setBrush(QColor('#d5cdc9'))
            self.box_markers[box_id] = marker

    def draw_agents(self):
        x_coords, y_coords = self._game_instance.player.pos()
        self.player_marker.setPos(x_coords*100-35, y_coords*-100-35)
        for box_id in self._game_instance.boxes:
            x_coords, y_coords = self._game_instance.boxes[box_id].pos()
            self.box_markers[box_id].setPos(x_coords*100-35, y_coords*-100-35)

    def restart_level(self, level=None):
        # @TODO zmienic kkopie fasf uprzatnac przekazywanie danych z game do gui pls
        self._game_instance.load_level(*get_level(1))
        move_counter = self.ui.moveCounter
        move_counter.setText(f'Moves: {self._game_instance.moves}')
        self.setup_level()
        self.draw_agents()


class Menu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


class PassScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_PassWindow()
        self.pc = 1
        self.ui.setupUi(self)
        # self.ui.nextLevelButton.clicked.connect(self.go_to_level)

    def go_to_level(self):
        try:
            self.pc += 1
            self.parent().game_window._game_instance.load_level(*get_level(self.pc))
            self.parent_.setup_level()
            # self.parent_.setup_tiles()
            # self.parent_.setup_boxes()
            self.parent().game_window.draw_agents()
            self.parent().setCurrentIndex(1)
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
    pass_window = PassScreen()
    gui = Gui(menu_window, game_window, pass_window)
    if not stack.objectName():
        stack.setObjectName(u"stack")
    stack.resize(800, 800)

    # stack.setStyleSheet(u"QWidget#stack {background-color: rgba(0, 200, 127, 255)}")

    # stack.addWidget(menu_window)
    # stack.addWidget(game_window)
    # stack.addWidget(pass_window)
    # menu_window.stack = stack
    # game_window.stack = stack
    # pass_window.stack = stack
    # stack.show()
    gui.show()
    # pass_window.ui.nextLevelButton.clicked.connect(pass_window.go_to_level)
    # gui.ui.stackedWidget.setCurrentIndex(0)
    # gui.ui.stackedWidget.setCurrentIndex(0)
    # game_window.show()
    # menu_window.show()
    return app.exec()


if __name__ == '__main__':

    gui_main(sys.argv)
