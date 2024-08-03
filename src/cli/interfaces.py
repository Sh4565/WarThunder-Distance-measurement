
import os
import cv2
import mss
import time
import numpy
import mouse
import keyboard
import settings

from pymenu import Menu
from pathlib import Path
from settings import config
from utils import screenrecord
from objects import Map, BoundingBox
from services.minimap import detect_map
from services.distance_calculation import distance_calculation
from services.find_objects import find_me, find_point, find_square


def play():
    minimap = Map()
    size_square = minimap.size_square_update

    sct = mss.mss()

    if size_square:
        print(f'Размер квадрата: {int(size_square)}x{int(size_square)}')
        print(f'Дистанция до цели:  ', end='\r')

    else:
        print(f'Размер квадрата: ')
        print(f'Дистанция до цели:  ', end='\r')
    while True:

        img = numpy.asarray(sct.grab(minimap.get.get))
        me = find_me(img)
        point = find_point(img)
        square = find_square(img)

        if size_square and square:
            minimap.scale = size_square / square
            distance = distance_calculation(me, point, img, minimap)

            spaces = ' ' * 8
            print(f'Дистанция до цели: {distance} {spaces}', end='\r')

        if keyboard.is_pressed('q'):
            cv2.destroyAllWindows()
            main_menu()

        if keyboard.is_pressed('u'):
            os.system('cls')
            print('Обновляю данные ...')
            size_square = minimap.size_square_update
            os.system('cls')
            print(f'Размер квадрата: {int(size_square)}x{int(size_square)}')
            spaces = ' ' * 8
            print(f'Дистанция до цели: {spaces}', end='\r')

        mode = screenrecord(img=img)
        if mode is None:
            main_menu(title='Ошибка! Карта не найдена.')


def find_minimap():
    print('Нажмите сочетание клавиш Shift + Win + S и выделите карту (с зазорами)')

    keyboard.wait('shift+win+s')

    press_time = None
    mouse_pressed = False
    left = None
    top = None
    while True:
        if keyboard.is_pressed('q'):
            cv2.destroyAllWindows()
            menu_settings()

        if mouse.is_pressed('left'):
            if not mouse_pressed:
                mouse_pressed = True
                press_time = time.time()
                left, top = mouse.get_position()

        if not mouse.is_pressed('left') and mouse_pressed:
            mouse_pressed = False
            release_time = time.time()
            right, bottom = mouse.get_position()
            hold_duration = release_time - press_time
            if hold_duration >= 1 and left and top:
                break

    mode = True
    while mode:
        mon = BoundingBox(top=top, left=left, width=bottom - top, height=right - left)

        mini_map = detect_map(mon)

        if mini_map:
            os.system('cls')
            print('Проверьте успешность определение карты.')
            print('Должно появиться окно вашей миникарты без зазоров.')
            print('В случае если есть дефекты нажмите клавишу "r" для повторного определения миникарты, или же повторите процедуру выделения.')
            print('Для завершение просмотра и сохранение данных нажмите клавишу "Enter"')

            mode = screenrecord(mon=mini_map.get)
            if mode is None:
                menu_settings(title='Ошибка! Карта не найдена.')
        else:
            mode = False

    menu_settings(title='Карта успешно найдена!')


def choose_who():
    if settings.WHO == 'Я':
        settings.WHO = 'Союзник'
        hsv_min = tuple(map(int, config.get('Ally', 'hsv_min').split(', ')))
        hsv_max = tuple(map(int, config.get('Ally', 'hsv_max').split(', ')))

        config.set('Settings', 'who', '0')
        config.set('Who', 'hsv_min', ', '.join(map(str, hsv_min)))
        config.set('Who', 'hsv_max', ', '.join(map(str, hsv_max)))
    else:
        settings.WHO = 'Я'
        hsv_min = tuple(map(int, config.get('Me', 'hsv_min').split(', ')))
        hsv_max = tuple(map(int, config.get('Me', 'hsv_max').split(', ')))

        config.set('Settings', 'who', '1')
        config.set('Who', 'hsv_min', ', '.join(map(str, hsv_min)))
        config.set('Who', 'hsv_max', ', '.join(map(str, hsv_max)))

    with open(Path(settings.BASE_DIR, 'config.cfg'), 'w') as f:
        config.write(f)

    menu_settings()


def choose_point():
    if settings.POINT == 'Желтая метка':
        settings.POINT = 'Красная метка'
        hsv_min = tuple(map(int, config.get('RedPoint', 'hsv_min').split(', ')))
        hsv_max = tuple(map(int, config.get('RedPoint', 'hsv_max').split(', ')))

        config.set('Settings', 'point', '0')
        config.set('Point', 'hsv_min', ', '.join(map(str, hsv_min)))
        config.set('Point', 'hsv_max', ', '.join(map(str, hsv_max)))
    else:
        settings.POINT = 'Желтая метка'
        hsv_min = tuple(map(int, config.get('YellowPoint', 'hsv_min').split(', ')))
        hsv_max = tuple(map(int, config.get('YellowPoint', 'hsv_max').split(', ')))

        config.set('Settings', 'point', '1')
        config.set('Point', 'hsv_min', ', '.join(map(str, hsv_min)))
        config.set('Point', 'hsv_max', ', '.join(map(str, hsv_max)))

    with open(Path(settings.BASE_DIR, 'config.cfg'), 'w') as f:
        config.write(f)

    menu_settings()


def menu_settings(title: str = ''):
    menu = Menu(title)
    menu.add_option("Ручное определение место положение миникарты", find_minimap)
    menu.add_option(f"Стрелок: {settings.WHO}", choose_who)
    menu.add_option(f"Цель: {settings.POINT}", choose_point)
    menu.add_option("Сменить язык", lambda: None)
    menu.add_option("Назад", main_menu)
    menu.show()


def main_menu(title: str = ''):
    menu = Menu(title)
    menu.add_option("Игра", play)
    menu.add_option("Настройки", menu_settings)
    menu.add_option("Exit", lambda: exit())
    menu.show()
