
from .play import play
from pymenu import Menu
from .settings_menu import menu_settings


def main_menu(title: str = ''):
    menu = Menu(title)
    menu.add_option("Игра", lambda: play(main_menu))
    menu.add_option("Настройки", lambda: menu_settings(main_menu))
    menu.add_option("Exit", lambda: exit())
    menu.show()


if __name__ == '__main__':
    main_menu()
