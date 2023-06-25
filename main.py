import sys

from PySide6.QtWidgets import QApplication

import game
from gui import MainWindow
from settings import Settings

if __name__ == '__main__':
    settings = Settings(random=False, file="words.txt", letters=5, max_words=6)

    error = game.load(settings)
    if error:
        print(error, file=sys.stderr)
        exit(1)
    app = QApplication()
    main_window = MainWindow(settings)
    main_window.show()
    app.exec()
