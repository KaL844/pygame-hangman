from typing import TypedDict
import pygame
from components.component import Component
from utils.enum_types import AlignType

from utils.logger import Logger
from utils.transform import TransformUtils

class ImageConf(TypedDict):
    src: str
    x: int
    y: int
    anchor: AlignType
    isVisible: bool

class Image(Component):
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_SRC = None
    DEFAULT_ANCHOR = AlignType.TOP_LEFT
    DEFAULT_VISIBLE = True

    logger = Logger(__name__).getInstance()

    def __init__(self, conf: ImageConf) -> None:
        print(conf)
        super().__init__(conf['x'] if 'x' in conf else Image.DEFAULT_X, conf['y'] if 'y' in conf else Image.DEFAULT_Y, 
            conf['isVisible'] if 'isVisbile' in conf else Image.DEFAULT_VISIBLE)
        self.src = conf['src'] if 'src' in conf else Image.DEFAULT_SRC
        self.anchor = AlignType[conf['anchor']] if 'anchor' in conf else Image.DEFAULT_ANCHOR
        
        self.image = None

        self.loadImg()


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
        