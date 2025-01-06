from PySide6.QtWidgets import QApplication, QGraphicsScene, QWidget
from PySide6.QtWidgets import QMainWindow

from headers.ui_sokobon import Ui_gameWindow
from headers.ui_menu import Ui_Menu
from headers.ui_pass_screen import Ui_PassWindow
from headers.ui_gui import Ui_MainWindow
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QTimer
from classes import Game
from level import get_level
import sys


GAME_SCALE = 1
BTN_SIZE = 35 * GAME_SCALE
AGENT_SIZE = 15 * GAME_SCALE
TILE_SIZE = 50 * GAME_SCALE


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
        self.pc = 1

        play = self.menu.ui.playButton
        play.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.pass_window.ui.nextLevelButton.clicked.connect(self.go_to_level)
        self.menu.ui.quitButton.clicked.connect(self.close)

    def go_to_level(self):

        try:
            self.pc += 1
            self.pass_window.ui.moveCounter.setText(
                str(self.game_window._game.moves))
            self.game_window._game.load_level(*get_level(self.pc))
            self.game_window.setup_level()
            self.game_window.draw_agents()
            self.ui.stackedWidget.setCurrentIndex(1)
        except FileNotFoundError:
            self.ui.stackedWidget.widget(0).ui.playButton.hide()
            win_text = 'Congrats you passed\n my Sokoban game'
            win_color = 'color: gold'
            self.ui.stackedWidget.widget(0).ui.label.setText(win_text)
            self.ui.stackedWidget.widget(0).ui.label.setStyleSheet(win_color)

            self.ui.stackedWidget.setCurrentIndex(0)


class GameWindow(QWidget):
    def __init__(self, game, parent=None):
        super().__init__(parent)
        self.ui = Ui_gameWindow()
        self.ui.setupUi(self)
        # czy game nie powinno byc publiczne
        self._scene = QGraphicsScene()
        self._game = game
        self._box_markers = {}
        self.setup_level()
        self.restart_level()

        self.ui.resetButton.clicked.connect(self.restart_level)
        self.ui.undoButton.clicked.connect(self.undo_move)

    def undo_move(self):
        self._game.valid_undo()
        self.draw_agents()
        # move counter do funkcji najlepiej jakiejs do rysowania
        move_counter = self.ui.moveCounter
        move_counter.setText(f'Moves: {self._game.moves}')

    @staticmethod
    def _format_size(size):
        return -size, -size, size, size

    @staticmethod
    def _format_position(x_coords, y_coords, object_size):
        offset = (TILE_SIZE-object_size)/2
        return x_coords*TILE_SIZE-offset, y_coords*-TILE_SIZE-offset

    def setup_level(self):
        self.setup_tiles()
        fsize = self._format_size
        self.player_marker = self._scene.addEllipse(*fsize(AGENT_SIZE))
        self.player_marker.setBrush(QColor("#0000ff"))
        self.setup_boxes()

    def setup_tiles(self):
        self._scene.clear()
        self.ui.levelView.setScene(self._scene)
        level = self._game.level
        fsize = self._format_size
        for tile_id in level:
            x_coords, y_coords = tile_id
            marker = self._scene.addRect(*fsize(TILE_SIZE))
            marker.setPos(x_coords*TILE_SIZE, y_coords*-TILE_SIZE)
            marker.setBrush(QColor("#eeeeee"))
            if str(level[tile_id]) == 'unknown':
                marker.setBrush(QColor("#444444"))
            elif str(level[tile_id]) == 'button':
                fposition = self._format_position
                marker = self._scene.addRect(*fsize(BTN_SIZE))
                marker.setPos(*fposition(x_coords, y_coords, BTN_SIZE))
                marker.setBrush(QColor("#ff0000"))

        label = self.ui.levelLabel
        label.setText(self._game.title)
        move_counter = self.ui.moveCounter
        move_counter.setText(f'Moves: {self._game.moves}')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.restart_level()
        elif event.key() == Qt.Key_U:
            self._game.valid_undo()
        else:
            # to chyba mozna wydzilic
            # mv = {
            #     Qt.Key_R: self.restart_level(),
            #     Qt.Key_U: self._game.valid_undo()
            # }
            self._game.validate_move(event.text())

        self.draw_agents()
        if self._game.game_ended():
            end_text = 'You finished in {moves_num} moves'
            self.parent().widget(2).ui.moveCounter.setText(end_text.format(
                moves_num=self._game.moves))

            QTimer.singleShot(400, lambda: self.parent().setCurrentIndex(2))
            # @todo mozna to z gui albo next level z next level
        move_counter = self.ui.moveCounter
        move_counter.setText(f'Moves: {self._game.moves}')
        return super().keyPressEvent(event)

    def setup_boxes(self):
        for box_id in self._game.boxes:
            fsize = self._format_size
            marker = self._scene.addRect(*fsize(AGENT_SIZE))
            marker.setBrush(QColor('#d5cdc9'))
            self._box_markers[box_id] = marker

    def draw_agents(self):
        x_coords, y_coords = self._game.player.pos()
        fposition = self._format_position
        self.player_marker.setPos(*fposition(x_coords, y_coords, AGENT_SIZE))
        for box_id in self._game.boxes:
            x_coords, y_coords = self._game.boxes[box_id].pos()
            self._box_markers[box_id].setPos(*fposition(x_coords,
                                                        y_coords,
                                                        AGENT_SIZE))

    def restart_level(self):
        level = self._game.title[6:]
        self._game.load_level(*get_level(level))
        move_counter = self.ui.moveCounter
        move_counter.setText(f'Moves: {self._game.moves}')
        self.setup_level()
        self.draw_agents()


class Menu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Menu()
        self.ui.setupUi(self)


class PassScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_PassWindow()
        # self.pc = 1
        self.ui.setupUi(self)

        # self.ui.nextLevelButton.clicked.connect(self.go_to_level)
# @TODO tu goto nie potrzebne

    def go_to_level(self):
        try:
            self.pc += 1
            self.parent().game_window._game.load_level(*get_level(self.pc))
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
    menu_window = Menu()
    game_window = GameWindow(game)
    pass_window = PassScreen()
    gui = Gui(menu_window, game_window, pass_window)

    gui.show()

    return app.exec()


if __name__ == '__main__':

    gui_main(sys.argv)
