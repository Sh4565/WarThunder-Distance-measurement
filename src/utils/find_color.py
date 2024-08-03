
import cv2
import mss
import numpy
import keyboard


def main(top: int, left: int, width: int, height: int) -> None:
    monitor = {
        'top': top,
        'left': left,
        'width': width,
        'height': height
    }

    cv2.namedWindow("result")
    cv2.namedWindow("settings")

    cv2.createTrackbar('h1', 'settings', 0, 255, lambda: None)
    cv2.createTrackbar('s1', 'settings', 0, 255, lambda: None)
    cv2.createTrackbar('v1', 'settings', 0, 255, lambda: None)
    cv2.createTrackbar('h2', 'settings', 255, 255, lambda: None)
    cv2.createTrackbar('s2', 'settings', 255, 255, lambda: None)
    cv2.createTrackbar('v2', 'settings', 255, 255, lambda: None)

    sct = mss.mss()
    while True:

        img = numpy.asarray(sct.grab(monitor))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        h1 = cv2.getTrackbarPos('h1', 'settings')
        s1 = cv2.getTrackbarPos('s1', 'settings')
        v1 = cv2.getTrackbarPos('v1', 'settings')
        h2 = cv2.getTrackbarPos('h2', 'settings')
        s2 = cv2.getTrackbarPos('s2', 'settings')
        v2 = cv2.getTrackbarPos('v2', 'settings')

        h_min = numpy.array((h1, s1, v1), numpy.uint8)
        h_max = numpy.array((h2, s2, v2), numpy.uint8)

        thresh = cv2.inRange(hsv, h_min, h_max)

        cv2.imshow('Origin', img)
        cv2.imshow('result', thresh)

        cv2.waitKey(5)
        if keyboard.is_pressed('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main(top=732, left=1572, width=340, height=342)
