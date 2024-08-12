
import cv2
import numpy
import requests

from objects.data_classes import HSV, ObjectMap
from settings.config import ObjectsConf, SettingsConf


class Shooter(ObjectMap):
    def __init__(self):
        super().__init__()
        self.__config = ObjectsConf()
        self.__settings = SettingsConf()

        self.shooter_type = self.__settings.shooter_type

        self.bgr = self.__config.get_shooter(self.__settings.shooter_type)['bgr']
        hsv_min = self.__config.get_shooter(self.__settings.shooter_type)['hsv_min']
        hsv_max = self.__config.get_shooter(self.__settings.shooter_type)['hsv_max']

        self.hsv = HSV(hsv_min, hsv_max)

    def find_shooter(self, img: numpy.ndarray) -> bool:
        h_min = numpy.array(self.hsv.min, numpy.uint8)
        h_max = numpy.array(self.hsv.max, numpy.uint8)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, h_min, h_max)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)

            m = cv2.moments(largest_contour)
            if m["m00"] != 0:
                center_x = int(m["m10"] / m["m00"])
                center_y = int(m["m01"] / m["m00"])

                self.x = center_x
                self.y = center_y

                cv2.circle(img, (center_x, center_y), 1, self.bgr, 2)

                return True

            else:
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                center_x = int(((x + w) + x) / 2)
                center_y = int(((y + h) + y) / 2)

                self.x = center_x
                self.y = center_y

                cv2.circle(img, (center_x, center_y), 1, self.bgr, 2)

                return True

        else:
            return False

    # TODO: Повысить точность определение игрока используя API
    # Этот прикол работает только с 2v генерации карт
    @staticmethod
    def get_shooter(minimap):
        map_objects = requests.get('http://localhost:8111/map_obj.json').json()
        map_info = requests.get('http://localhost:8111/map_info.json').json()

        if map_objects and map_info:
            for map_object in map_objects:
                if map_object['icon'] == 'Player':
                    absolut_x = map_object['x'] * map_info['grid_size'][0]
                    absolut_y = map_object['y'] * map_info['grid_size'][1]

                    scale_x = minimap.width / map_info['grid_size'][0]
                    scale_y = minimap.height / map_info['grid_size'][1]

                    x = absolut_x * scale_x
                    y = absolut_y * scale_y

                    return x, y
            return False
