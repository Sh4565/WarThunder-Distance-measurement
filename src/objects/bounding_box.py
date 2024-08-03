
class BoundingBox:
    def __init__(self, top, left, width, height):
        self._top = top
        self._left = left
        self._width = width
        self._height = height

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
    def get(self) -> dict:
        return {
            'top': self._top,
            'left': self._left,
            'width': self._width,
            'height': self._height,
        }

    def __str__(self) -> str:
        return f"""{{
    top: {self.top}
    left: {self.left}
    width: {self.width}
    height: {self.height}
}}"""
