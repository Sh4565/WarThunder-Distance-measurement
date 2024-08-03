
import settings
import requests

from pathlib import Path
from typing import Optional
from settings import config
from .data_classes import HSV
from .bounding_box import BoundingBox


class Map:
    def __init__(self):
        self.name = None
        self.scale = None
        self.size_square = None

        self._config = config

        self.top = self._config.getint('Map', 'top')
        self.left = self._config.getint('Map', 'left')
        self.width = self._config.getint('Map', 'width')
        self.height = self._config.getint('Map', 'height')

        hsv_min = tuple(map(int, self._config.get('Map', 'hsv_min').split(', ')))
        hsv_max = tuple(map(int, self._config.get('Map', 'hsv_max').split(', ')))

        self.hsv = HSV(
            hsv_min,
            hsv_max
        )

    @property
    def size_square_update(self) -> Optional[int]:
        map_info = requests.get('http://localhost:8111/map_info.json').json()

        if map_info['valid'] is True:
            x = map_info['grid_steps'][0]
            y = map_info['grid_steps'][1]

            self.size_square = x

            return self.size_square
        else:
            return None

    @property
    def get(self) -> BoundingBox:
        return BoundingBox(self.top, self.left, width=self.width, height=self.height)

    def set(self, minimap: BoundingBox) -> None:
        self.top = minimap.top
        self.left = minimap.left
        self.width = minimap.width
        self.height = minimap.height

        self._config.set('Map', 'top', str(self.top))
        self._config.set('Map', 'left', str(self.left))
        self._config.set('Map', 'width', str(self.width))
        self._config.set('Map', 'height', str(self.height))

        with open(Path(settings.BASE_DIR, 'config.cfg'), 'w') as f:
            self._config.write(f)
