from PySide6.QtWidgets import QApplication, QGraphicsScene, QWidget
from PySide6.QtWidgets import QMainWindow

from headers.ui_sokoban import Ui_gameWindow
from headers.ui_menu import Ui_Menu
from headers.ui_pass_screen import Ui_PassWindow
from headers.ui_gui import Ui_MainWindow
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtCore import Qt, QTimer, Signal
from model import Game
from load_level import get_level
import sys


GAME_SCALE = 1
BTN_SIZE = 32 * GAME_SCALE
AGENT_SIZE = 32 * GAME_SCALE
TILE_SIZE = 50 * GAME_SCALE


class Menu(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Menu()
        self.ui.setupUi(self)

    def show_win_screen(self) -> None:
        self.ui.playButton.hide()
        win_text = 'Congrats you passed\n my Sokoban game'
        win_color = 'color: gold'
        self.ui.label.setText(win_text)
        self.ui.label.setStyleSheet(win_color)


class PassScreen(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_PassWindow()
        self.ui.setupUi(self)

    def pass_message(self, moves_num: int) -> None:
        move_counter = self.ui.moveCounter
        end_text = 'You finished in {moves_num} moves'
        move_counter.setText(end_text.format(moves_num=moves_num))


class GameWindow(QWidget):
    end_signal = Signal(int)

    def __init__(self, game: Game, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_gameWindow()
        self.ui.setupUi(self)

        self._scene = QGraphicsScene()
        self._game = game
        self._box_markers = {}
        self._setup_level()
        self._draw_agents()

        self.ui.resetButton.clicked.connect(self.restart_level)
        self.ui.undoButton.clicked.connect(self._undo_move)

    @staticmethod
    def _format_size(size: int) -> tuple[int, int, int, int]:
        return -size, -size, size, size

    @staticmethod
    def _format_position(x_coords: int, y_coords: int, object_size: int
                         ) -> tuple[float, float]:
        offset = (TILE_SIZE-object_size)/2
        return x_coords*TILE_SIZE-offset, y_coords*-TILE_SIZE-offset

    def _setup_tiles(self) -> None:
        self.ui.levelView.setScene(self._scene)
        tiles = self._game.tiles
        fsize = self._format_size
        for tile_id in tiles:
            x_coords, y_coords = tile_id
            marker = self._scene.addRect(*fsize(TILE_SIZE))
            marker.setPos(x_coords*TILE_SIZE, y_coords*-TILE_SIZE)
            marker.setBrush(QColor("#eeeeee"))
            if str(tiles[tile_id]) == 'wall':
                marker.setBrush(QColor("#444444"))
            elif str(tiles[tile_id]) == 'button':
                fposition = self._format_position
                button_sprite = QPixmap('assets/button.png')
                marker = self._scene.addPixmap(button_sprite)
                marker.setPos(*fposition(x_coords, y_coords, -BTN_SIZE))

        label = self.ui.levelLabel
        label.setText(self._game.title)

    def _setup_boxes(self) -> None:
        for box_id in self._game.boxes:
            box_sprite = QPixmap('assets/box.png')
            marker = self._scene.addPixmap(box_sprite)
            self._box_markers[box_id] = marker

    def _draw_agents(self) -> None:
        x_coords, y_coords = self._game.player.pos
        fposition = self._format_position
        self._player_marker.setPos(*fposition(x_coords, y_coords, -AGENT_SIZE))
        for box_id in self._game.boxes:
            x_coords, y_coords = self._game.boxes[box_id].pos
            self._box_markers[box_id].setPos(*fposition(x_coords,
                                                        y_coords,
                                                        -AGENT_SIZE))
        move_counter = self.ui.moveCounter
        move_counter.setText(f'Moves: {self._game.moves_num}')

    def _setup_level(self) -> None:
        self._scene.clear()
        self._setup_tiles()
        player_sprite = QPixmap('assets/player.png')
        self._player_marker = self._scene.addPixmap(player_sprite)
        self._setup_boxes()

    def restart_level(self) -> None:
        level_id = self._game.level_id
        self._game.load_level(level_id, *get_level(level_id))
        self._setup_level()
        self._draw_agents()

    def next_level(self):
        self._game.increment_level_id()
        self.restart_level()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_R:
            self.restart_level()
        elif event.key() == Qt.Key_U:
            self._game.undo_move()
        else:
            self._game.move(event.text().lower())

        self._draw_agents()
        if self._game.game_ended():
            event.ignore()
            moves = self._game.moves_num
            QTimer.singleShot(400, lambda: self.end_signal.emit(moves))
        return super().keyPressEvent(event)

    def _undo_move(self) -> None:
        self._game.undo_move()
        self._draw_agents()


class Gui(QMainWindow):
    def __init__(self,
                 menu: Menu,
                 game_window: GameWindow,
                 pass_window: PassScreen,
                 parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.stackedWidget.addWidget(menu)
        self.ui.stackedWidget.addWidget(game_window)
        self.ui.stackedWidget.addWidget(pass_window)
        self._pass_window = pass_window
        self._menu = menu
        self._game_window = game_window

        play = self._menu.ui.playButton
        play.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self._menu.ui.quitButton.clicked.connect(self.close)

        end_signal = self._game_window.end_signal
        end_signal.connect(self.go_to_pass_window)

        self._pass_window.ui.nextLevelButton.clicked.connect(self.go_to_game)

    def go_to_pass_window(self, moves_num: int) -> None:
        self._pass_window.pass_message(moves_num)
        self.ui.stackedWidget.setCurrentIndex(2)

    def go_to_game(self) -> None:

        try:
            self._game_window.next_level()
            self.ui.stackedWidget.setCurrentIndex(1)
        except FileNotFoundError:
            self._menu.show_win_screen()
            self.ui.stackedWidget.setCurrentIndex(0)


def gui_main(argv):
    app = QApplication(argv)
    game = Game(0, *get_level(0))
    menu_window = Menu()
    game_window = GameWindow(game)
    pass_window = PassScreen()
    gui = Gui(menu_window, game_window, pass_window)

    gui.show()
    return app.exec()


if __name__ == '__main__':
    gui_main(sys.argv)
