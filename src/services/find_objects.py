
import cv2
import numpy

from typing import Optional
from objects import Me, Point, Square


def find_me(img: numpy.ndarray) -> Optional[Me]:
    me = Me()

    h_min = numpy.array(me.hsv.min, numpy.uint8)
    h_max = numpy.array(me.hsv.max, numpy.uint8)

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

            cv2.circle(img, (center_x, center_y), 2, me.bgr, 2)

            me.x = center_x
            me.y = center_y

            return me
        else:
            return None
    else:
        return None


def find_point(img: numpy.ndarray) -> Optional[Point]:
    point = Point()

    h_min = numpy.array(point.hsv.min, numpy.uint8)
    h_max = numpy.array(point.hsv.max, numpy.uint8)

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

            cv2.circle(img, (center_x, center_y), 1, point.bgr, 2)

            point.x = center_x
            point.y = center_y

            return point
        else:
            return None
    else:
        return None


def find_square(img: numpy.ndarray) -> Optional[int]:
    square = Square()

    h_min = numpy.array(square.hsv.min, numpy.uint8)
    h_max = numpy.array(square.hsv.max, numpy.uint8)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, h_min, h_max)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    largest_contour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(largest_contour)
    square.x1 = x
    square.y1 = y
    square.x2 = x + w
    square.y2 = y + h

    cv2.line(img, (x, y + h), (x + w, y + h), square.bgr, thickness=3)

    return max(w, h)
