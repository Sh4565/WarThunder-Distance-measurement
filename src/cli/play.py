
import os
import cv2
import mss
import time
import numpy
import keyboard

from objects import Map, Shooter, Point
from utils.screenrecord import screenrecord
from settings.config import SettingsConf, KeyboardsConf


def play(main_menu):
    config = SettingsConf()
    keyboards = KeyboardsConf()

    _ = config.lang

    minimap = Map()
    shooter = Shooter()
    point = Point()

    size_square_px, size_square_m = minimap.size_square_update
    sct = mss.mss()

    print(_('Размер квадрата: {size_square_m}x{size_square_m}').format(size_square_m=int(size_square_m)))
    print(_('Дистанция до цели:  '), end='\r')

    start_time = 0
    current_time = 0
    while True:
        img = numpy.asarray(sct.grab(minimap.get.get))

        if keyboard.is_pressed(keyboards.calculating_distance):
            start_time = time.time()

        shooter.find_shooter(img)
        point.find_point(img)

        if size_square_m and size_square_px and shooter.x and shooter.y and point.x and point.y:
            minimap.scale = size_square_m / size_square_px

            distance = minimap.distance_calculation(shooter, point)
            minimap.display_distance(img, shooter, point, distance)
            # distance = distance_calculation(shooter, point, img, minimap)
            spaces = ' ' * 8
            print(_('Дистанция до цели: {distance} {spaces}').format(distance=distance, spaces=spaces), end='\r')
        #
        # if current_time - start_time <= config.delay:
        #     shooter.find_shooter(img)
        #     point.find_point(img)
        #
        #     if size_square_m and size_square_px and shooter.x and shooter.y:
        #         minimap.scale = size_square_m / size_square_px
        #         distance = distance_calculation(shooter, point, img, minimap)
        #         spaces = ' ' * 8
        #         print(f'Дистанция до цели: {distance} {spaces}', end='\r')

        if keyboard.is_pressed(keyboards.close_minimap):
            cv2.destroyAllWindows()
            main_menu()

        if keyboard.is_pressed(keyboards.update_data):
            os.system('cls')
            print(_('Обновляю данные ...'))
            size_square_px, size_square_m = minimap.size_square_update
            os.system('cls')
            print(_('Размер квадрата: {size_square_m}x{size_square_m}').format(size_square_m=int(size_square_m)))
            spaces = ' ' * 8
            print(_('Дистанция до цели: {spaces}').format(spaces=spaces), end='\r')

        mode = screenrecord(img=img)
        if mode is None:
            cv2.destroyAllWindows()
            main_menu(title=_('Ошибка! Карта не найдена.'))

        current_time = time.time()
