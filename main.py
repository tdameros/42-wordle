import PySide6
import sys
import string
import random
from dataclasses import dataclass
from enum import Enum

char_count = 5

choosen = None
words = None

class CharacterStatus(Enum):
    CORRECT = 1
    WRONG_PLACE = 2
    INCORRECT = 3

@dataclass
class Character:
    char: str # char
    status: CharacterStatus

    def __str__(self):
        match self.status:
            case CharacterStatus.CORRECT:
                return f"\033[32m{self.char}\033[0m"
            case CharacterStatus.WRONG_PLACE:
                return f"\033[33m{self.char}\033[0m"
            case _:
                return f"\033[38m{self.char}\033[0m"

def analyse(input: str) -> list[Character] | None:
    if (len(input) != char_count) or (input not in words):
        return None

    tmp: list[str | None] = [c for c in choosen]
    result: list[Character | None] = [None] * char_count

    for i in range(len(input)):
        if input[i] == tmp[i]:
            result[i] = Character(input[i], CharacterStatus.CORRECT)
            tmp[i] = None

    for i in range(len(input)):
        if (not result[i]) and (input[i] in tmp):
            result[i] = Character(input[i], CharacterStatus.WRONG_PLACE)
            tmp[tmp.index(input[i])] = None

    for i in range(len(input)):
        if not result[i]:
            result[i] = Character(input[i], CharacterStatus.INCORRECT)

    return result

def load(filename: string) -> str | None:
    global words
    global choosen

    f = open(filename, "r")
    lines: list[str] = f.readlines()
    words = [x.strip() for x in lines if x.strip()]
    if not len(words):
        return "Empty database"
    elif any(x for x in words if len(x) != char_count):
        return "Some words are not 5 characters"
    elif any(word for word in words if not all((letter in string.ascii_lowercase) for letter in word)):
        return "Some words are not using alphabetic symbols [a-z]"
    choosen = random.choice(words)
    return None

if __name__ == "__main__":
    error = load("words.txt")
    if error:
        print(error, file=sys.stderr)
        exit(1)

    # open_window()
    while 1:
        val = input("Enter your value: ")
        print(''.join(c.__str__() for c in (analyse(val) or "")))
