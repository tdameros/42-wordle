from dataclasses import dataclass

@dataclass
class Settings:
    random: bool
    file: str
    max_words: int
    letters: int
