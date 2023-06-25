import string
import random
import datetime
from dataclasses import dataclass
from enum import Enum
from settings import Settings

choosen: str = None
words: list[str] = None

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
    global settings

    if (input not in words):
        return None

    tmp: list[str | None] = [c for c in choosen]
    result: list[Character | None] = [None] * len(input)

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


def load(filename: string, settings: Settings) -> str | None:
    global words
    global choosen

    f = open(filename, "r")
    lines: list[str] = f.readlines()
    words = [x.strip() for x in lines if x.strip()]
    if not len(words):
        return "Empty database"
    elif any(x for x in words if len(x) != settings.letters):
        return f"Some words are not {settings.letters} characters"
    elif any(word for word in words if not all((letter in string.ascii_lowercase) for letter in word)):
        return "Some words are not using alphabetic symbols [a-z]"

    if settings.random:
        choosen = random.choice(words)
    else:
        date = datetime.datetime.now()
        index = date.year * 100000 + date.month * 1000 + date.day
        index %= len(words)
        choosen = words[index]

    return None
