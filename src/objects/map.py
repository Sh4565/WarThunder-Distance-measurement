
import numpy
import requests
import configparser

from typing import Optional
from .data_classes import HSV
from .bounding_box import BoundingBox
from settings import CONFIG_PATH_OBJECTS


class Map:
    def __init__(self):
        self.name = None
        self.scale = None
        self.size_square_m = None
        self.size_square_px = None

        self._config = configparser.ConfigParser()
        self._config.read(CONFIG_PATH_OBJECTS)

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
    def size_square_update(self) -> (Optional[int], Optional[int]):
        try:
            map_info = requests.get('http://localhost:8111/map_info.json').json()

            if map_info['valid'] is True:
                x = map_info['grid_steps'][0]
                y = map_info['grid_steps'][1]

                self.size_square_m = max(x, y)

                grid_size = numpy.array(map_info["grid_size"])
                grid_steps = numpy.array(map_info["grid_steps"])

                steps = grid_size / grid_steps

                step_size_minimap = self.width / steps

                self.size_square_px = max(step_size_minimap)

                return self.size_square_px, self.size_square_m

            else:
                return 0, 0
        except requests.exceptions.ConnectionError:
            return 0, 0

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

        with open(CONFIG_PATH_OBJECTS, 'w') as f:
            self._config.write(f)
