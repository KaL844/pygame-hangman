import pygame
from components.component import Component


class Panel(Component):
    DEFAULT_X = 0
    DEFAULT_Y = 0

    def __init__(self, conf: dict = None, x: int = DEFAULT_X, y: int = DEFAULT_Y) -> None:
        self.children: dict[str, Component] = {}

        if (conf is not None):
            self._initWithConf(conf)
        else:
            self._initWithParams(x, y)

    def _initWithConf(self, conf: dict):
        super().__init__(conf["posX"] if "posX" in conf else Panel.DEFAULT_X, conf["posY"] if "posY" in conf else Panel.DEFAULT_Y)

    def _initWithParams(self, x: int, y: int) -> None:
        super().__init__(x, y)

    def draw(self, screen: pygame.surface.Surface) -> None:
        for child in self.children.values():
            child.draw(screen)

    def addChild(self, name: str, child: Component) -> None:
        child.setPosition(child.x + self.x, child.y + self.y)
        self.children[name] = child

    def setPosition(self, x: int, y: int) -> None:
        dx = x - self.x
        dy = y - self.y
        for child in self.children.values():
            child.setPosition(child.x + dx, child.y + dy)
        return super().setPosition(x, y)

    def clear(self) -> None:
        self.children = {}