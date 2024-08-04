
import mss
import cv2
import numpy
import keyboard

from objects import Map, BoundingBox


def detect_map(area, stability_threshold=5) -> Map or False:

    sct = mss.mss()
    minimap = Map()

    stable_count = 0
    last_coordinates = None

    bar = ['\\', '|', '/', '-']
    lk = 0
    mode = True
    print('Наведетесь на небо чтобы мини карта была на синем фоне. Чтобы прервать нажмите "Esc"')
    while mode:
        print(f'Поиск карты {bar[lk]} ', end='\r')

        if lk != 3:
            lk += 1
        else:
            lk = 0

        img = numpy.asarray(sct.grab(area.get))

        h_min = numpy.array(minimap.hsv.min, numpy.uint8)
        h_max = numpy.array(minimap.hsv.max, numpy.uint8)
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

                minimap.set(BoundingBox(
                    top=screen_top,
                    left=screen_left,
                    width=screen_width,
                    height=screen_height
                ))

                cv2.destroyAllWindows()
                return minimap

        cv2.imshow('Tactical map', img)
        cv2.waitKey(25)
        if keyboard.is_pressed('esc'):
            cv2.destroyAllWindows()
            return False

    return False
