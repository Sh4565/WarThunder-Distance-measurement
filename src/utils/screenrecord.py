
import mss
import cv2
import numpy
import keyboard
import configparser

from typing import Optional
from objects import BoundingBox
from settings import CONFIG_PATH_SETTINGS


def screenrecord(img: numpy.ndarray = None, mon: BoundingBox = None) -> Optional[bool]:
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH_SETTINGS)

        map_redefinition = config.get('Keyboard', 'map_redefinition').lower()

        if img is not None:
            cv2.imshow('Tactical map', img)
            cv2.waitKey(25)
            if keyboard.is_pressed('l'):
                cv2.destroyAllWindows()
                return False

            elif keyboard.is_pressed('k'):
                cv2.destroyAllWindows()
                return True

            else:
                return True

        elif mon is not None:
            monitor = {
                'top': mon.top,
                'left': mon.left,
                'width': mon.width,
                'height': mon.height
            }

            sct = mss.mss()
            while True:
                img = numpy.asarray(sct.grab(monitor))

                cv2.imshow('Tactical map', img)
                if keyboard.is_pressed('enter'):
                    cv2.destroyAllWindows()
                    return False
                if keyboard.is_pressed(map_redefinition):
                    cv2.destroyAllWindows()
                    return True

                cv2.waitKey(25)

    except mss.exception.ScreenShotError:
        return None
