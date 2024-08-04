
import configparser

from objects.data_classes import HSV
from settings import CONFIG_PATH_OBJECTS, CONFIG_PATH_SETTINGS


class Shooter:
    def __init__(self):
        self.x = None
        self.y = None

        self._config = configparser.ConfigParser()
        self._config.read(CONFIG_PATH_OBJECTS)

        self.bgr = tuple(map(int, self._config.get('Shooter', 'bgr').split(', ')))

    @staticmethod
    def create_shooter():
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH_SETTINGS)
        shooter_type = config.get('Settings', 'shooter_type').lower()

        if shooter_type == 'me':
            return Me()
        elif shooter_type == 'ally':
            return Ally()
        else:
            raise ValueError(f"Unknown shooter type: {shooter_type}")


class Me(Shooter):
    def __init__(self):
        super().__init__()
        hsv_min = tuple(map(int, self._config.get('Me', 'hsv_min').split(', ')))
        hsv_max = tuple(map(int, self._config.get('Me', 'hsv_max').split(', ')))
        self.hsv = HSV(hsv_min, hsv_max)


class Ally(Shooter):
    def __init__(self):
        super().__init__()
        hsv_min = tuple(map(int, self._config.get('Ally', 'hsv_min').split(', ')))
        hsv_max = tuple(map(int, self._config.get('Ally', 'hsv_max').split(', ')))
        self.hsv = HSV(hsv_min, hsv_max)
