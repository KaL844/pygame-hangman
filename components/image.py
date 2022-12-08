import pygame
from components.component import Component
from utils.enum_types import AlignType

from utils.logger import Logger
from utils.transform import TransformUtils


class Image(Component):
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_SRC = None
    DEFAULT_ANCHOR = AlignType.TOP_LEFT

    logger = Logger(__name__).getInstance()

    def __init__(self, conf: dict = None, src: str = DEFAULT_SRC, x: int = DEFAULT_X, y: int = DEFAULT_Y, 
            anchor: AlignType = DEFAULT_ANCHOR) -> None:
        if (conf is not None):
            self._initWithConf(conf)
        else:
            self._initWithParams(src, x, y, anchor)
        
        self.image = None

        self.loadImg()

    def _initWithConf(self, conf: dict):
        super().__init__(conf["posX"] if "posX" in conf else Image.DEFAULT_X, conf["posY"] if "posY" in conf else Image.DEFAULT_Y)
        self.src = conf["src"] if "src" in conf else Image.DEFAULT_SRC
        self.anchor = AlignType[conf["anchor"]] if "anchor" in conf else Image.DEFAULT_ANCHOR

    def _initWithParams(self, src: str, x: int, y: int, anchor: AlignType) -> None:
        super().__init__(x, y)
        self.src = src
        self.anchor = anchor

    def draw(self, screen: pygame.surface.Surface) -> None:
        if self.image is None: return

        posX, posY = TransformUtils.alignAnchor(self.anchor, self.x, self.y, self.image.get_size()[0], self.image.get_size()[1])
        screen.blit(self.image, (posX, posY))

    def loadImg(self) -> None:
        if self.src is None:
            return
        self.image = pygame.image.load(self.src)

    def setSrc(self, src: str) -> None:
        self.src = src
        self.loadImg()
        