
import pygetwindow

from .bounding_box import BoundingBox


class Window:
    def __init__(self):
        window = pygetwindow.getWindowsWithTitle('War Thunder')[0]
        self.top = window.top
        self.left = window.left
        self.width = window.width
        self.height = window.height

    @property
    def get(self) -> BoundingBox:
        return BoundingBox(self.top, self.left, width=self.width, height=self.height)

    def __str__(self) -> str:
        return f"""{{
    top: {self.top}
    left: {self.left}
    width: {self.width}
    height: {self.height}
}}"""
