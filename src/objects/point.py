
import configparser

from objects.data_classes import HSV
from settings import CONFIG_PATH_OBJECTS, CONFIG_PATH_SETTINGS


class Point:
    def __init__(self):
        self.x = None
        self.y = None
        self._config = configparser.ConfigParser()
        self._config.read(CONFIG_PATH_OBJECTS)

        self.bgr = tuple(map(int, self._config.get('Point', 'bgr').split(', ')))

    @staticmethod
    def create_point():
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH_SETTINGS)
        point_type = config.get('Settings', 'point_type').lower()
        if point_type == 'red':
            return RedPoint()
        elif point_type == 'yellow':
            return YellowPoint()
        else:
            raise ValueError(f"Unknown point type: {point_type}")


class RedPoint(Point):
    def __init__(self):
        super().__init__()
        hsv_min = tuple(map(int, self._config.get('RedPoint', 'hsv_min').split(', ')))
        hsv_max = tuple(map(int, self._config.get('RedPoint', 'hsv_max').split(', ')))
        self.hsv = HSV(hsv_min, hsv_max)


class YellowPoint(Point):
    def __init__(self):
        super().__init__()
        hsv_min = tuple(map(int, self._config.get('YellowPoint', 'hsv_min').split(', ')))
        hsv_max = tuple(map(int, self._config.get('YellowPoint', 'hsv_max').split(', ')))
        self.hsv = HSV(hsv_min, hsv_max)
