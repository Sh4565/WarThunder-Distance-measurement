
import keyboard

from pymenu import Menu
from .find_map import find_minimap
from settings.config import KeyboardsConf, SettingsConf


type_key = None


def choose_shooter(main_menu):
    config = SettingsConf()
    config.next_shooter_type()

    menu_settings(main_menu)


def choose_point(main_menu):
    config = SettingsConf()
    config.next_point_type()

    menu_settings(main_menu)


def set_keyboard(main_menu, menu_settings, settings_keyboard, type_key):
    print('Нажмите кнопку. Для отмены нажмите "Esc"')

    keyboards = KeyboardsConf()

    while True:
        if keyboard.is_pressed('esc'):
            settings_keyboard(main_menu, menu_settings)

        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name != 'esc':
            if type_key == 'map_redefinition':
                keyboards.set_map_redefinition(event.name)
            if type_key == 'close_minimap':
                keyboards.set_close_minimap(event.name)
            if type_key == 'update_data':
                keyboards.set_update_data(event.name)
            if type_key == 'calculating_distance':
                keyboards.set_calculating_distance(event.name)
            settings_keyboard(main_menu, menu_settings)


def settings_keyboard(main_menu, menu_settings):
    keyboards = KeyboardsConf()

    map_redefinition = keyboards.map_redefinition
    close_minimap = keyboards.close_minimap
    update_data = keyboards.update_data
    calculating_distance = keyboards.calculating_distance

    menu = Menu('')
    menu.add_option(f"Переопределение карты: {map_redefinition}",
                    lambda: set_keyboard(main_menu, menu_settings, settings_keyboard, 'map_redefinition'))
    menu.add_option(f"Закрыть окно мини карты: {close_minimap}",
                    lambda: set_keyboard(main_menu, menu_settings, settings_keyboard, 'close_minimap'))
    menu.add_option(f"Обновить данные: {update_data}",
                    lambda: set_keyboard(main_menu, menu_settings, settings_keyboard, 'update_data'))
    menu.add_option(f"Вычисление дистанции: {calculating_distance}",
                    lambda: set_keyboard(main_menu, menu_settings, settings_keyboard, 'calculating_distance'))
    menu.add_option("Назад", lambda: menu_settings(main_menu))
    menu.show()


def menu_settings(main_menu, title: str = ''):
    config = SettingsConf()

    menu = Menu(title)
    menu.add_option("Ручное определение местоположения мини карты", lambda: find_minimap(main_menu, menu_settings))
    menu.add_option(f"Стрелок: {config.shooter_type}", lambda: choose_shooter(main_menu))
    menu.add_option(f"Цель: {config.point_type}", lambda: choose_point(main_menu))
    menu.add_option("Клавиатура", lambda: settings_keyboard(main_menu, menu_settings))
    menu.add_option("Назад", lambda: main_menu())
    menu.show()
