
import cv2
import numpy

from typing import Optional
from objects import Point, Shooter


def find_shooter(img: numpy.ndarray) -> Shooter:
    shooter = Shooter()
    shooter = shooter.create_shooter()

    h_min = numpy.array(shooter.hsv.min, numpy.uint8)
    h_max = numpy.array(shooter.hsv.max, numpy.uint8)

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

            cv2.circle(img, (center_x, center_y), 2, shooter.bgr, 2)

            shooter.x = center_x
            shooter.y = center_y

            return shooter

        else:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            center_x = int(((x + w) + x) / 2)
            center_y = int(((y + h) + y) / 2)

            cv2.circle(img, (center_x, center_y), 2, shooter.bgr, 2)

            shooter.x = center_x
            shooter.y = center_y

            return shooter

    else:
        return shooter


def find_point(img: numpy.ndarray) -> Optional[Point]:
    point = Point()
    point = point.create_point()

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
