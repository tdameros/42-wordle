import sys

from PySide6.QtWidgets import QApplication

import game
import gui

if __name__ == '__main__':
    error = game.load("words.txt")
    if error:
        print(error, file=sys.stderr)
        exit(1)
    app = QApplication()
    main_window = gui.MainWindow()
    main_window.show()
    app.exec()
