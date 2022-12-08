import pygame


class Component:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def draw(self, screen: pygame.surface.Surface) -> None:
        pass

    def setPosition(self, x: int, y: int) -> None:
        self.x = x
        self.y = y