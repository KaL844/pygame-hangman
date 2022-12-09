import pygame
from components.button import Button
from components.image import Image
from components.input import InputTextBox
from components.label import Label
from components.panel import Panel
from components.scene import Scene, SceneManager
from modules.game.logic import GameLogic
from utils.enum_types import AlignType, MouseEvent
from utils.json_reader import JsonReader
from utils.logger import Logger
import utils.constants as constants

class GameScene(Scene):
    _instance = None

    logger = Logger(__name__).getInstance()

    CONFIG_FILE = "conf/game/GameScene.json"
    RESOURCE_PATH = "res/game/"

    CURRENT_IMG_PREFIX = "hangman"
    CURRENT_IMG_SUFFIX = ".png"
    
    def __init__(self) -> None:
        GameScene._instance = self

        self.conf = JsonReader.load(GameScene.CONFIG_FILE)

        self.sceneMgr = None
        self.logic: GameLogic = GameLogic.getInstance()

        self.titleLabel: Label = Label(conf=self.conf["titleLabel"])
        self.answerLabel: Label = Label(conf=self.conf["answerLabel"])
        self.currentImg: Image = Image(conf=self.conf["currentImg"])
        self.alphabetPanel: Panel = Panel(conf=self.conf["alphabetPanel"])
        self.endGamePanel: Panel = Panel(conf=self.conf["endGamePanel"])
        self.returnBtn: Button = self.endGamePanel.getChild("returnBtn")
        self.messageLabel: Label = self.endGamePanel.getChild("messageLabel")
        self.isRunning: bool = True

        self.init()
        
    def init(self) -> None:
        self.sceneMgr = SceneManager.getInstance()

        self.returnBtn.addEventListener(MouseEvent.ON_TOUCH_END, self.onReturnClick)

    def onEnter(self) -> None:
        self.clear()

        self.logic.start()

        self.currentImg.setSrc(self.getCurrentImgSrc())
        self.loadAllChar()

    def input(self, event: pygame.event.Event) -> None:
        if not self.isRunning: return

        if event.type == pygame.KEYDOWN:
            isRightAnswer = self.logic.updateAnswer(event.unicode)

            self.loadAllChar()

            if not isRightAnswer:
                self.currentImg.setSrc(self.getCurrentImgSrc())

            if self.logic.isGameOver():
                GameScene.logger.info("GameScene.input. Game over")
                self.endGame()
                return        

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(constants.BACKGROUND_COLOR)

        self.titleLabel.draw(screen)

        self.answerLabel.setText(self.logic.getAnswer())
        self.answerLabel.draw(screen)

        self.currentImg.draw(screen)
        
        self.alphabetPanel.draw(screen)
        self.endGamePanel.draw(screen)

    def endGame(self) -> None:
        self.isRunning = False
        self.messageLabel.setText("Congratulation!!" if self.logic.isWon() else f"Your secret word is {self.logic.getSecretWord()}")
        self.endGamePanel.setVisible(True)

    def onReturnClick(self) -> None:
        self.sceneMgr.clear()
        from ..lobby.scenes import StartScene
        self.sceneMgr.push(StartScene.getInstance())

    def getCurrentImgSrc(self) -> str:
        return "{}{}{}{}".format(GameScene.RESOURCE_PATH, GameScene.CURRENT_IMG_PREFIX, self.logic.getGuessCount(), 
            GameScene.CURRENT_IMG_SUFFIX)

    def loadAllChar(self) -> None:
        self.alphabetPanel.clear()

        texts = self.logic.getAllChar().split("\n")
        for i, label in enumerate(texts):
            self.alphabetPanel.addChild(f"lable{i}", Label({"x": self.alphabetPanel.width // 2, "y": i * 30, "text": label, "anchor": "TOP_CENTER"}))

    def clear(self) -> None:
        self.isRunning = True
        self.alphabetPanel.clear()
        self.messageLabel.clearText()
        self.endGamePanel.setVisible(False)

    @staticmethod
    def getInstance() -> "GameScene":
        if GameScene._instance is None:
            GameScene()
        return GameScene._instance