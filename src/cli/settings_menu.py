
import keyboard
import configparser

from pymenu import Menu
from .find_map import find_minimap
from settings import CONFIG_PATH_SETTINGS


type_key = None


def choose_shooter(main_menu):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH_SETTINGS)

    shooter_type = config.get('Settings', 'shooter_type')

    if shooter_type == 'me':
        config.set('Settings', 'shooter_type', 'ally')
    elif shooter_type == 'ally':
        config.set('Settings', 'shooter_type', 'me')
    else:
        config.set('Settings', 'shooter_type', 'me')

    with open(CONFIG_PATH_SETTINGS, 'w') as f:
        config.write(f)

    menu_settings(main_menu)


def choose_point(main_menu):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH_SETTINGS)

    point_type = config.get('Settings', 'point_type')

    if point_type == 'yellow':
        config.set('Settings', 'point_type', 'red')
    elif point_type == 'red':
        config.set('Settings', 'point_type', 'yellow')
    else:
        config.set('Settings', 'point_type', 'yellow')

    with open(CONFIG_PATH_SETTINGS, 'w') as f:
        config.write(f)

    menu_settings(main_menu)


def set_keyboard(main_menu, menu_settings, settings_keyboard, type_key):
    print('Нажмите кнопку. Для отмены нажмите "Esc"')

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH_SETTINGS)

    while True:
        if keyboard.is_pressed('esc'):
            settings_keyboard(main_menu, menu_settings)

        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name != 'esc':
            config.set('Keyboard', type_key, event.name)
            with open(CONFIG_PATH_SETTINGS, 'w') as f:
                config.write(f)
            settings_keyboard(main_menu, menu_settings)


def settings_keyboard(main_menu, menu_settings):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH_SETTINGS)

    map_redefinition = config.get('Keyboard', 'map_redefinition').lower()
    close_minimap = config.get('Keyboard', 'close_minimap').lower()
    update_data = config.get('Keyboard', 'update_data').lower()
    calculating_distance = config.get('Keyboard', 'calculating_distance').lower()

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
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH_SETTINGS)

    point_type = config.get('Settings', 'point_type')
    shooter_type = config.get('Settings', 'shooter_type')

    menu = Menu(title)
    menu.add_option("Ручное определение местоположения мини карты", lambda: find_minimap(main_menu, menu_settings))
    menu.add_option(f"Стрелок: {shooter_type}", lambda: choose_shooter(main_menu))
    menu.add_option(f"Цель: {point_type}", lambda: choose_point(main_menu))
    menu.add_option("Клавиатура", lambda: settings_keyboard(main_menu, menu_settings))
    menu.add_option("Назад", lambda: main_menu())
    menu.show()
