import pygame
import typing
from components.component import Component

from utils.enum_types import MouseEvent
from utils.logger import Logger

pygame.init()
FONT = pygame.font.Font(None, 30)

class Button(Component):
    DEFAULT_COLOR = (255, 255, 255)
    DEFAULT_TEXT_COLOR = (0, 0, 0)
    DEFAULT_TEXT = ""
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_WIDTH = 180
    DEFAULT_HEIGHT = 40
    DEFAULT_VISIBLE = True

    logger = Logger(__name__).getInstance()

    def __init__(self, conf: dict = None, x: int = DEFAULT_X, y: int = DEFAULT_Y, text: str = DEFAULT_TEXT, 
            color: tuple[int, int, int] = DEFAULT_COLOR, textColor: tuple[int, int, int] = DEFAULT_TEXT_COLOR, 
            width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT, isVible: bool = DEFAULT_VISIBLE) -> None:

        self.isClicked: bool = False
        self.eventListeners: dict[MouseEvent, typing.Callable[[], None]] = {}

        if (conf is not None):
            self._initWithConf(conf)
        else:
            self._initWithParams(x, y, text, color, textColor, width, height, isVible)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def _initWithConf(self, conf: dict):
        Button.logger.info("Button._initWithConf. conf={}".format(conf))

        super().__init__(conf["posX"] if "posX" in conf else Button.DEFAULT_X, 
            conf["posY"] if "posY" in conf else Button.DEFAULT_Y)
        self.text = conf["text"] if "text" in conf else Button.DEFAULT_TEXT
        self.color = tuple(conf["color"]) if "color" in conf else Button.DEFAULT_COLOR
        self.textColor = conf["textColor"] if "textColor" in conf else Button.DEFAULT_TEXT_COLOR
        self.width = conf["width"] if "width" in conf else Button.DEFAULT_WIDTH
        self.height = conf["height"] if "height" in conf else Button.DEFAULT_HEIGHT
        self.isVisible = conf["isVisible"] if "isVisible" in conf else Button.DEFAULT_VISIBLE

    def _initWithParams(self, x: int, y: int, text: str, color: tuple[int, int, int], textColor: tuple[int, int, int], 
            width: int, height: int, isVisible: bool) -> None:
        super().__init__(x, y)
        self.text = text
        self.color = color
        self.textColor = textColor
        self.width = width
        self.height = height
        self.isVisible = isVisible

    def draw(self, screen: pygame.surface.Surface) -> None:
        if not self.isVisible: return

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.isClicked:
                self.isClicked = True
            
            if pygame.mouse.get_pressed()[0] == 0 and self.isClicked:
                self.isClicked = False
                if MouseEvent.ON_TOUCH_END in self.eventListeners: self.eventListeners[MouseEvent.ON_TOUCH_END]()

        pygame.draw.rect(screen, self.color, self.rect)

        textImg = FONT.render(self.text, True, self.textColor)
        screen.blit(textImg, (self.x + self.width // 2 - textImg.get_size()[0] // 2, self.y + self.height // 2 - textImg.get_size()[1] // 2))

    def addEventListener(self, event: MouseEvent, handler: typing.Callable[[], None]) -> None:
        self.eventListeners[event] = handler

    def setVisible(self, isVisible: bool) -> None:
        self.isVisible = isVisible
