
import os
import cv2
import time
import mouse
import keyboard

from utils import screenrecord
from objects import Map, BoundingBox
from settings.config import KeyboardsConf


def find_minimap(main_menu, menu_settings):
    keyboards = KeyboardsConf()

    print('Нажмите сочетание клавиш Shift + Win + S и выделите карту (с зазорами)')
    keyboard.wait('shift+win+s')

    press_time = None
    mouse_pressed = False
    left, top = None, None

    while True:
        if keyboard.is_pressed(keyboards.close_minimap):
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
        minimap = Map()
        minimap.detect_map(mon)
        # mini_map = detect_map(mon)

        if minimap:
            os.system('cls')
            print(f'''
Проверьте успешность определения карты.
Должно появиться окно вашей мини карты без зазоров.
В случае если есть дефекты нажмите клавишу {keyboards.map_redefinition} для повторного определения мини карты, 
или же повторите процедуру выделения.
Для завершения просмотра и сохранения данных нажмите клавишу "Enter"
            ''')

            mode = screenrecord(mon=minimap.get)
            if mode is None:
                menu_settings(main_menu, title='Ошибка! Карта не найдена.')
        else:
            mode = False

    menu_settings(main_menu, title='Карта успешно найдена!')
