
import configparser

from .main import CONFIG_PATH_OBJECTS


class ObjectsConf:
    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__config.read(CONFIG_PATH_OBJECTS)

    @property
    def get_map(self) -> dict:
        return {
            'top': self.__config.getint('Map', 'top'),
            'left': self.__config.getint('Map', 'left'),
            'width': self.__config.getint('Map', 'width'),
            'height': self.__config.getint('Map', 'height'),
            'hsv_min': tuple(map(int, self.__config.get('Map', 'hsv_min').split(', '))),
            'hsv_max': tuple(map(int, self.__config.get('Map', 'hsv_max').split(', ')))
        }

    def set_size_map(self, top, left, width, height) -> None:
        self.__config.set('Map', 'top', str(top))
        self.__config.set('Map', 'left', str(left))
        self.__config.set('Map', 'width', str(width))
        self.__config.set('Map', 'height', str(height))

        with open(CONFIG_PATH_OBJECTS, 'w') as f:
            self.__config.write(f)

    def get_shooter(self, shooter_type: str) -> dict:
        return {
            'bgr': tuple(map(int, self.__config.get('Shooter', 'bgr').split(', '))),
            'hsv_min': tuple(map(int, self.__config.get(shooter_type, 'hsv_min').split(', '))),
            'hsv_max': tuple(map(int, self.__config.get(shooter_type, 'hsv_max').split(', '))),
        }

    def get_point(self, point_type: str) -> dict:
        return {
            'bgr': tuple(map(int, self.__config.get('Point', 'bgr').split(', '))),
            'hsv_min': tuple(map(int, self.__config.get(point_type, 'hsv_min').split(', '))),
            'hsv_max': tuple(map(int, self.__config.get(point_type, 'hsv_max').split(', '))),
        }
