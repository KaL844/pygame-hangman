from enum import Enum
import pygame

class ComponentType(Enum):
    Button = "Button"
    Image = "Image"
    Label = "Label"

class Component:
    def __init__(self, x: int, y: int, isVisible: bool) -> None:
        self.x = x
        self.y = y
        self.isVisible = isVisible

    def draw(self, screen: pygame.surface.Surface) -> None:
        pass

    def setPosition(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def setVisible(self, isVisible: bool) -> None:
        self.isVisible = isVisible

    @staticmethod
    def getComponent(type: ComponentType, conf: dict) -> "Component":
        if type == ComponentType.Button:
            from components.button import Button
            return Button(conf=conf)
        if type == ComponentType.Label:
            from components.label import Label
            return Label(conf=conf)