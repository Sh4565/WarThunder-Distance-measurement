
import cv2
import math
import numpy

from typing import Optional
from objects.data_classes import HSV, ObjectMap
from settings.config import ObjectsConf, SettingsConf


class Point(ObjectMap):
    def __init__(self):
        super().__init__()

        self.__config = ObjectsConf()
        self.__settings = SettingsConf()

        self.bgr = self.__config.get_point(self.__settings.point_type)['bgr']
        hsv_min = self.__config.get_point(self.__settings.point_type)['hsv_min']
        hsv_max = self.__config.get_point(self.__settings.point_type)['hsv_max']

        self.hsv = HSV(hsv_min, hsv_max)

    def find_point(self, img: numpy.ndarray) -> Optional[tuple]:
        h_min = numpy.array(self.hsv.min, numpy.uint8)
        h_max = numpy.array(self.hsv.max, numpy.uint8)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, h_min, h_max)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)

            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)

            if perimeter == 0:
                return None

            circularity = (4 * math.pi * area) / (perimeter * perimeter)

            if circularity > 0.85:
                m = cv2.moments(largest_contour)
                if m["m00"] != 0:
                    center_x = int(m["m10"] / m["m00"])
                    center_y = int(m["m01"] / m["m00"])

                    cv2.circle(img, (center_x, center_y), 1, self.bgr, 2)

                    self.x = center_x
                    self.y = center_y

                return self.x, self.y
            else:
                return None
        else:
            return None
