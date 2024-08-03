
import pygetwindow

from .bounding_box import BoundingBox


class Window:
    def __init__(self):
        window = pygetwindow.getWindowsWithTitle('War Thunder')[0]
        self._top = window.top
        self._left = window.left
        self._width = window.width
        self._height = window.height

    @property
    def top(self) -> int:
        return self._top

    @property
    def left(self) -> int:
        return self._left

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def get(self) -> BoundingBox:
        return BoundingBox(self._top, self._left, width=self._width, height=self._height)

    def __str__(self) -> str:
        return f"""{{
    top: {self.top}
    left: {self.left}
    width: {self.width}
    height: {self.height}
}}"""
