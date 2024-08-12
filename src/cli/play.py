
import os
import time

import cv2
import mss
import numpy
import keyboard

from utils import screenrecord
from objects import Map, Shooter, Point
from settings.config import SettingsConf, KeyboardsConf


def play(main_menu):
    config = SettingsConf()
    keyboards = KeyboardsConf()

    minimap = Map()
    shooter = Shooter()
    point = Point()

    size_square_px, size_square_m = minimap.size_square_update
    sct = mss.mss()

    print(f'Размер квадрата: {int(size_square_m)}x{int(size_square_m)}')
    print(f'Дистанция до цели:  ', end='\r')

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
            print(f'Дистанция до цели: {distance} {spaces}', end='\r')
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
            print('Обновляю данные ...')
            size_square_px, size_square_m = minimap.size_square_update
            os.system('cls')
            print(f'Размер квадрата: {int(size_square_m)}x{int(size_square_m)}')
            spaces = ' ' * 8
            print(f'Дистанция до цели: {spaces}', end='\r')

        mode = screenrecord(img=img)
        if mode is None:
            cv2.destroyAllWindows()
            main_menu(title='Ошибка! Карта не найдена.')

        current_time = time.time()
