
import cv2
import math
import numpy

from objects import Map
from objects import Me, Point


def distance_calculation(me: Me, point: Point, img: numpy.ndarray, minimap: Map) -> str:

    if me and point:
        cv2.circle(img, (me.x, me.y), 2, me.bgr, 2)
        cv2.circle(img, (point.x, point.y), 2, point.bgr, 2)
        cv2.line(img, (me.x, me.y), (point.x, point.y), (255, 255, 0), thickness=1)

        mid_x = (me.x + point.x) // 2
        mid_y = (me.y + point.y) // 2

        if me.x >= point.x:
            x1 = point.x
            x2 = me.x
        else:
            x1 = me.x
            x2 = point.x

        if me.y >= point.y:
            y1 = point.y
            y2 = me.y
        else:
            y1 = me.y
            y2 = point.y

        distance = int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * minimap.scale)

        text = f"{distance}m"

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4
        color = (0, 0, 0)
        thickness = 1

        cv2.putText(img, text, (mid_x, mid_y), font, font_scale, color, thickness, cv2.LINE_AA)

        return f'{distance}m'

    else:
        return ''
