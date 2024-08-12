
import cv2
import mss
import math
import numpy
import requests
import keyboard

from .point import Point
from typing import Optional
from .shooter import Shooter
from .bounding_box import BoundingBox
from settings.config import ObjectsConf
from .data_classes import HSV, ObjectMap


class Map:
    def __init__(self):
        self.name = None
        self.scale = None
        self.size_square_m = None
        self.size_square_px = None

        self.steps = None
        self.grid_zero = None
        self.step_size_minimap = None
        self.map_max = None

        self.__config = ObjectsConf()

        self.top = self.__config.get_map['top']
        self.left = self.__config.get_map['left']
        self.width = self.__config.get_map['width']
        self.height = self.__config.get_map['height']

        hsv_min = self.__config.get_map['hsv_min']
        hsv_max = self.__config.get_map['hsv_max']

        self.hsv = HSV(
            hsv_min,
            hsv_max
        )

    @property
    def size_square_update(self) -> (Optional[int], Optional[int]):
        try:
            map_info = requests.get('http://localhost:8111/map_info.json').json()

            if map_info['valid'] is True:
                self.grid_zero = map_info['grid_steps']
                self.map_max = map_info['map_max']

                self.size_square_m = max(self.grid_zero[0], self.grid_zero[1])

                grid_size = numpy.array(map_info["grid_size"])
                grid_steps = numpy.array(map_info["grid_steps"])

                self.steps = grid_size / grid_steps
                self.step_size_minimap = self.width / self.steps
                self.size_square_px = max(self.step_size_minimap)

                self.scale = self.size_square_m / self.size_square_px

                return self.size_square_px, self.size_square_m

            else:
                return 0, 0
        except requests.exceptions.ConnectionError:
            return 0, 0

    @property
    def get(self) -> BoundingBox:
        return BoundingBox(self.top, self.left, width=self.width, height=self.height)

    def detect_map(self, area, stability_threshold=5) -> bool:
        sct = mss.mss()

        stable_count = 0
        last_coordinates = None

        bar = ['\\', '|', '/', '-']
        lk = 0
        print('Наведитесь на небо чтобы мини карта была на синем фоне. Чтобы прервать нажмите "Esc"')

        while True:
            print(f'Поиск карты {bar[lk]} ', end='\r')

            if lk != 3:
                lk += 1
            else:
                lk = 0

            img = numpy.asarray(sct.grab(area.get))

            h_min = numpy.array(self.hsv.min, numpy.uint8)
            h_max = numpy.array(self.hsv.max, numpy.uint8)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            thresh = cv2.inRange(hsv, h_min, h_max)

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
            closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

            contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            all_points_list = []

            for cnt in contours:
                reshaped_cnt = cnt.reshape(-1, 2)
                all_points_list.append(reshaped_cnt)

            if all_points_list:
                all_points = numpy.vstack(all_points_list)

                x, y, w, h = cv2.boundingRect(all_points)

                size = max(w, h)
                x = x - (size - w) // 2
                y = y - (size - h) // 2
                w = h = size

                current_coordinates = (x, y, w, h)
                if last_coordinates is None or current_coordinates == last_coordinates:
                    stable_count += 1
                else:
                    stable_count = 0

                last_coordinates = current_coordinates

                if stable_count >= stability_threshold:
                    stable_coordinates = current_coordinates
                    top, left, width, height = stable_coordinates
                    cv2.rectangle(img, (top, left), (top + width, left + height), (0, 0, 255), thickness=2)

                    screen_top = area.top + y
                    screen_left = area.left + x
                    screen_width = width - 3
                    screen_height = height - 3

                    self.top = screen_top
                    self.left = screen_left
                    self.width = screen_width
                    self.height = screen_height

                    self.__config.set_size_map(self.top, self.left, self.width, self.height)
                    return True

            if keyboard.is_pressed('esc'):
                return False

    def distance_calculation(self, obj1: ObjectMap, obj2: ObjectMap) -> int:

        if obj1.x >= obj2.x:
            x1 = obj2.x
            x2 = obj1.x
        else:
            x1 = obj1.x
            x2 = obj2.x

        if obj1.y >= obj2.y:
            y1 = obj2.y
            y2 = obj1.y
        else:
            y1 = obj1.y
            y2 = obj2.y

        distance = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * self.scale)

        return distance

    @staticmethod
    def display_distance(img: numpy.ndarray, shooter: Shooter, point: Point, distance: int):

        text = f"{distance}m"

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4
        color = (0, 255, 0)
        thickness = 1

        mid_x = (shooter.x + point.x) // 2
        mid_y = (shooter.y + point.y) // 2

        cv2.circle(img, (shooter.x, shooter.y), 2, shooter.bgr, 2)
        cv2.circle(img, (point.x, point.y), 2, point.bgr, 2)
        cv2.line(img, (shooter.x, shooter.y), (point.x, point.y), (255, 255, 0), thickness=1)
        cv2.putText(img, text, (mid_x, mid_y), font, font_scale, color, thickness, cv2.LINE_AA)

    def set(self, minimap: BoundingBox) -> None:
        self.top = minimap.top
        self.left = minimap.left
        self.width = minimap.width
        self.height = minimap.height

        self.__config.set_size_map(self.top, self.left, self.width, self.height)
