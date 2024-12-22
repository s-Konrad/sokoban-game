from PySide2.QtWidgets import QApplication, QWidget, QMainWindow
from ui_sokobon import Ui_MainWindow
import sys


class Gui(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


def gui_main(args):
    app = QApplication(args)
    window = Gui()
    window.show()
    return app.exec_()


if __name__ == '__main__':
    gui_main(sys.argv)
