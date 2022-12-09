from typing import TypedDict
import pygame
from components.component import Component, ComponentType
from utils.enum_types import AlignType
from utils.transform import TransformUtils

class PanelConf(TypedDict):
    x: int; y: int
    width: int; height: int
    backgroundColor: tuple[int, int, int, int]
    anchor: AlignType
    isVisible: bool
    children: dict

class Panel(Component):
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_WIDTH = 0
    DEFAULT_HEIGHT = 0
    DEFAULT_BACKGROUND_COLOR = (0, 0, 0, 0)
    DEFAULT_ANCHOR = AlignType.TOP_LEFT
    DEFAULT_VISIBLE = True

    def __init__(self, conf: PanelConf) -> None:
        self.children: dict[str, Component] = {}

        super().__init__(conf["x"] if "x" in conf else Panel.DEFAULT_X, conf["y"] if "y" in conf else Panel.DEFAULT_Y, 
            conf["isVisible"] if "isVisible" in conf else Panel.DEFAULT_VISIBLE)
        if "children" in conf:
            children: dict = conf["children"]
            for childName, child in children.items():
                self.addChild(childName, Component.getComponent(ComponentType[child["component"]], child))
        self.width = conf["width"] if "width" in conf else Panel.DEFAULT_WIDTH
        self.height = conf["height"] if "height" in conf else Panel.DEFAULT_HEIGHT
        self.backgroundColor = conf["backgroundColor"] if "backgroundColor" in conf else Panel.DEFAULT_BACKGROUND_COLOR
        self.anchor = AlignType[conf["anchor"]] if "anchor" in conf else Panel.DEFAULT_ANCHOR

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

    def draw(self, screen: pygame.surface.Surface) -> None:
        if not self.isVisible: return 

        self.surface.fill(self.backgroundColor)

        for child in self.children.values():
            child.draw(self.surface)

        posX, posY = TransformUtils.alignAnchor(self.anchor, self.x, self.y, self.width, self.height)
        screen.blit(self.surface, (posX, posY))

    def addChild(self, name: str, child: Component) -> None:
        self.children[name] = child

    def getChild(self, name: str) -> Component:
        if name in self.children: return self.children[name]

    def clear(self) -> None:
        self.children = {}