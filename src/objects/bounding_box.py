
class BoundingBox:
    def __init__(self, top, left, width, height):
        self.top = top
        self.left = left
        self.width = width
        self.height = height

    @property
    def get(self) -> dict:
        return {
            'top': self.top,
            'left': self.left,
            'width': self.width,
            'height': self.height,
        }

    def __str__(self) -> str:
        return f"""{{
    top: {self.top}
    left: {self.left}
    width: {self.width}
    height: {self.height}
}}"""
