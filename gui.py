from enum import Enum

from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt

import game


class BoxStyleSheet(Enum):
    EMPTY = """
        background-color: #121213;
        border: 2px solid #3A3A3C;
        font-size: 42px;
        font-weight: bold;
        color: white;
    """
    FILLED = """
        background-color: #121213;
        border: 2px solid #565758;
        font-size: 42px;
        font-weight: bold;
        color: white;
    """
    CORRECT = """
        background-color: #528C4D;
        font-size: 42px;
        font-weight: bold;
        color: white;
    """
    WRONG_PLACE = """
        background-color: #B69E3C;
        font-size: 42px;
        font-weight: bold;
        color: white;
    """
    INCORRECT = """
        background-color: #565758;
        font-size: 42px;
        font-weight: bold;
        color: white;
    """


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.width = 500
        self.height = 600
        self.box_size = 80
        self.max_word = 6
        self.max_letter = 5

        self.word_count = 0
        self.letter_count = 0
        self.current_word = ""

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Wordle")
        self.setMinimumSize(500, 600)
        self.setMaximumSize(500, 600)
        self.layout = QGridLayout()
        self.setStyleSheet("""
        background-color: #121213;
        """)
        self.boxes = []
        for y in range(self.max_word):
            for x in range(self.max_letter):
                box = self.create_box("", self.box_size)
                self.boxes.append(box)
                self.layout.addWidget(box, y, x)
        self.setLayout(self.layout)

    @staticmethod
    def create_box(letter: str, size: int) -> QLabel:
        box = QLabel(letter)
        box.setAlignment(Qt.AlignCenter)
        box.width = size
        box.height = size
        box.setStyleSheet(BoxStyleSheet.EMPTY.value)
        return box

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.delete_letter()
        elif event.key() == Qt.Key_Return:
            self.check_word()
        elif len(event.text()) > 0:
            self.add_letter(event.text()[0].lower())

    def get_current_box(self):
        return self.boxes[self.word_count * self.max_letter + self.letter_count]

    def get_previous_box(self):
        if self.letter_count == 0:
            return None
        return self.boxes[self.word_count * self.max_letter + self.letter_count - 1]

    def delete_letter(self):
        box = self.get_previous_box()
        if box is not None:
            box.setText("")
            box.setStyleSheet(BoxStyleSheet.EMPTY.value)
            self.letter_count -= 1
            self.current_word = self.current_word[:-1]

    def add_letter(self, letter: str):
        if letter.isalpha() and self.letter_count < self.max_letter:
            box = self.get_current_box()
            box.setText(letter.upper())
            box.setStyleSheet(BoxStyleSheet.FILLED.value)
            self.letter_count += 1
            self.current_word += letter

    def check_word(self):
        game_analyse = game.analyse(self.current_word)
        if self.letter_count == self.max_letter and game_analyse is not None:
            self.color_letters(game_analyse)
            if game.choosen == self.current_word:
                self.launch_exit_box(True)
            self.letter_count = 0
            self.current_word = ""
            self.word_count += 1
            if self.word_count == self.max_word:
                self.launch_exit_box(False)

    def color_letters(self, game_analyse):
        for i in range(self.max_letter):
            self.letter_count = i
            box = self.get_current_box()
            if game_analyse[i].status == game.CharacterStatus.INCORRECT:
                box.setStyleSheet(BoxStyleSheet.INCORRECT.value)
            elif game_analyse[i].status == game.CharacterStatus.WRONG_PLACE:
                box.setStyleSheet(BoxStyleSheet.WRONG_PLACE.value)
            elif game_analyse[i].status == game.CharacterStatus.CORRECT:
                box.setStyleSheet(BoxStyleSheet.CORRECT.value)

    @staticmethod
    def launch_exit_box(win: bool):
        dialog_box = QMessageBox()
        if win:
            dialog_box.setText("Winner!")
        else:
            dialog_box.setText("Looser!")
        dialog_box.exec_()
        exit(0)

