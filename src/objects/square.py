
import settings

from objects.data_classes import HSV


class Square:
    def __init__(self):
        self.x = None
        self.y = None

        self._config = settings.config

        self.bgr = tuple(map(int, self._config.get('Square', 'bgr').split(', ')))

        hsv_min = tuple(map(int, self._config.get('Square', 'hsv_min').split(', ')))
        hsv_max = tuple(map(int, self._config.get('Square', 'hsv_max').split(', ')))

        self.hsv = HSV(
            hsv_min,
            hsv_max
        )
