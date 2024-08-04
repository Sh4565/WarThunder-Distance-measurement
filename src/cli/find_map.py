
import os
import cv2
import time
import mouse
import keyboard
import configparser

from utils import screenrecord
from objects import BoundingBox
from services.minimap import detect_map
from settings import CONFIG_PATH_SETTINGS


def find_minimap(main_menu, menu_settings):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH_SETTINGS)

    close_minimap = config.get('Keyboard', 'close_minimap').lower()
    map_redefinition = config.get('Keyboard', 'map_redefinition').lower()

    print('Нажмите сочетание клавиш Shift + Win + S и выделите карту (с зазорами)')
    keyboard.wait('shift+win+s')

    press_time = None
    mouse_pressed = False
    left, top = None, None

    while True:
        if keyboard.is_pressed(close_minimap):
            cv2.destroyAllWindows()
            menu_settings(main_menu)

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
            print(f'''
Проверьте успешность определения карты.
Должно появиться окно вашей мини карты без зазоров.
В случае если есть дефекты нажмите клавишу {map_redefinition} для повторного определения мини карты, или же повторите процедуру
выделения.
Для завершения просмотра и сохранения данных нажмите клавишу "Enter"
            ''')

            mode = screenrecord(mon=mini_map.get)
            if mode is None:
                menu_settings(main_menu, title='Ошибка! Карта не найдена.')
        else:
            mode = False

    menu_settings(main_menu, title='Карта успешно найдена!')
