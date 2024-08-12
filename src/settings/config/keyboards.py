
import configparser

from .main import CONFIG_PATH_SETTINGS


class KeyboardsConf:
    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__config.read(CONFIG_PATH_SETTINGS)

    @property
    def map_redefinition(self) -> str:
        return self.__config.get('Keyboard', 'map_redefinition').lower()

    @property
    def close_minimap(self) -> str:
        return self.__config.get('Keyboard', 'close_minimap').lower()

    @property
    def update_data(self) -> str:
        return self.__config.get('Keyboard', 'update_data').lower()

    @property
    def calculating_distance(self) -> str:
        return self.__config.get('Keyboard', 'calculating_distance').lower()

    def set_map_redefinition(self, key: str) -> None:
        self.__config.set('Keyboard', 'map_redefinition', key)
        with open(CONFIG_PATH_SETTINGS, 'w') as f:
            self.__config.write(f)

    def set_close_minimap(self, key: str) -> None:
        self.__config.set('Keyboard', 'close_minimap', key)
        with open(CONFIG_PATH_SETTINGS, 'w') as f:
            self.__config.write(f)

    def set_update_data(self, key: str) -> None:
        self.__config.set('Keyboard', 'update_data', key)
        with open(CONFIG_PATH_SETTINGS, 'w') as f:
            self.__config.write(f)

    def set_calculating_distance(self, key: str) -> None:
        self.__config.set('Keyboard', 'calculating_distance', key)
        with open(CONFIG_PATH_SETTINGS, 'w') as f:
            self.__config.write(f)

