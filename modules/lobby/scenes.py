import pygame
from components.button import Button
from components.scene import Scene, SceneManager
from modules.game.scenes import GameScene
from utils.enum_types import MouseEvent
from utils.json_reader import JsonReader
import utils.constants as constants


class StartScene(Scene):
    CONFIG_FILE = "conf/lobby/StartScene.json"

    _instance = None

    def __init__(self) -> None:
        StartScene._instance = self

        self.sceneMgr = None

        self.conf = JsonReader.load(StartScene.CONFIG_FILE)

        self.startBtn: Button = Button(conf=self.conf["startBtn"])

        self.init()

    def init(self) -> None:
        self.sceneMgr = SceneManager.getInstance()

        self.startBtn.addEventListener(MouseEvent.ON_TOUCH_END, self.onStartClick)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(constants.BACKGROUND_COLOR)
        self.startBtn.draw(screen)

    def onStartClick(self):
        self.sceneMgr.push(GameScene.getInstance())

    @staticmethod
    def getInstance():
        if (StartScene._instance == None):
            StartScene()
        return StartScene._instance