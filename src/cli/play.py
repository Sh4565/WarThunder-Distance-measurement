
import os
import time

import cv2
import mss
import numpy
import keyboard
import configparser


from objects import Map
from utils import screenrecord
from settings import CONFIG_PATH_SETTINGS
from services.distance_calculation import distance_calculation
from services.find_objects import find_point, find_shooter


def play(main_menu):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH_SETTINGS)

    close_minimap = config.get('Keyboard', 'close_minimap').lower()
    update_data = config.get('Keyboard', 'update_data').lower()
    calculating_distance = config.get('Keyboard', 'calculating_distance').lower()
    delay = config.getfloat('Settings', 'delay')

    minimap = Map()
    size_square_px, size_square_m = minimap.size_square_update
    sct = mss.mss()

    print(f'Размер квадрата: {int(size_square_m)}x{int(size_square_m)}')
    print(f'Дистанция до цели:  ', end='\r')

    start_time = 0
    current_time = 0
    while True:
        img = numpy.asarray(sct.grab(minimap.get.get))

        if keyboard.is_pressed(calculating_distance):
            start_time = time.time()

        if current_time - start_time <= delay:
            me = find_shooter(img)
            point = find_point(img)

            if size_square_m and size_square_px and me.x and me.y:
                minimap.scale = size_square_m / size_square_px
                distance = distance_calculation(me, point, img, minimap)
                spaces = ' ' * 8
                print(f'Дистанция до цели: {distance} {spaces}', end='\r')

        if keyboard.is_pressed(close_minimap):
            cv2.destroyAllWindows()
            main_menu()

        if keyboard.is_pressed(update_data):
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
