
import cv2
import math
import numpy

from objects import Map
from objects import Shooter, Point


def distance_calculation(shooter: Shooter, point: Point, img: numpy.ndarray, minimap: Map) -> str:

    if shooter and point:
        cv2.circle(img, (shooter.x, shooter.y), 2, shooter.bgr, 2)
        cv2.circle(img, (point.x, point.y), 2, point.bgr, 2)
        cv2.line(img, (shooter.x, shooter.y), (point.x, point.y), (255, 255, 0), thickness=1)

        mid_x = (shooter.x + point.x) // 2
        mid_y = (shooter.y + point.y) // 2

        if shooter.x >= point.x:
            x1 = point.x
            x2 = shooter.x
        else:
            x1 = shooter.x
            x2 = point.x

        if shooter.y >= point.y:
            y1 = point.y
            y2 = shooter.y
        else:
            y1 = shooter.y
            y2 = point.y

        distance = int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * minimap.scale)

        text = f"{distance}m"

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4
        color = (0, 255, 0)
        thickness = 1

        cv2.putText(img, text, (mid_x, mid_y), font, font_scale, color, thickness, cv2.LINE_AA)

        return f'{distance}m'

    else:
        return ''
