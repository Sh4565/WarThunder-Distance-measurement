
import sys

from .play import play
from pymenu import Menu
from settings import SettingsConf
from .settings_menu import menu_settings


def main_menu(title: str = ''):
    _ = SettingsConf().lang
    menu = Menu(title)
    menu.add_option(_("Игра"), lambda: play(main_menu))
    menu.add_option(_("Настройки"), lambda: menu_settings(main_menu))
    menu.add_option(_("Выход"), lambda: sys.exit())
    menu.show()


if __name__ == '__main__':
    main_menu()
