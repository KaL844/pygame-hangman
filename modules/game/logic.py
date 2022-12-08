import random

from random_word import RandomWords
from utils.logger import Logger

class GameLogic:
    _instance = None

    ALL_CHAR = [
        "A", "B", "C", "D", "E", "F", "J", "H", "I", "J", "K", "L", "M", "N", "O", "P",
        "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    ]

    UNDEFINE_CHAR = "-"
    MAX_WRONG_GUESS = 5

    logger = Logger(__name__).getInstance()
    
    def __init__(self) -> None:
        GameLogic._instance = self
        
        self.random = RandomWords()
        self.secretWord = ""
        self.answer: list[str] = []
        self.guessed: set[str] = set()
        self.guessCount = 0

    def start(self) -> None:
        self.secretWord: str = self.random.get_random_word()
        self.secretWord = self.secretWord.upper()

        self.guessCount = 0
        self.guessed: set[str] = set()
        self.answer = [GameLogic.UNDEFINE_CHAR for _ in self.secretWord]
        GameLogic.logger.info("GameLogic.start. secretWord={}".format(self.secretWord))

    def updateAnswer(self, char: str) -> bool:
        char = char.upper()
        self.guessed.add(char)
        if char not in self.secretWord:
            self.guessCount += 1
            return False
        for i, c in enumerate(self.secretWord):
            if c == char: self.answer[i] = c
        return True

    def getAnswer(self) -> str:
        return " ".join(self.answer)

    def isGameOver(self) -> bool:
        GameLogic.logger.info("GameLogic.isGameOver. answer={}".format(self.answer))
        return self.guessCount > GameLogic.MAX_WRONG_GUESS or GameLogic.UNDEFINE_CHAR not in self.answer

    def getGuessCount(self) -> int:
        return self.guessCount

    def getAllChar(self) -> str:
        string = ""
        for i, char in enumerate(GameLogic.ALL_CHAR):
            string += char if char not in self.guessed else "#"

            if i % 10 == 9:
                string += "\n"
            else:
                string += " "
        return string

    def getInstance() -> "GameLogic":
        if GameLogic._instance is None:
            GameLogic()
        return GameLogic._instance