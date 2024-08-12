
import configparser

from .main import CONFIG_PATH_SETTINGS


class SettingsConf:
    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__config.read(CONFIG_PATH_SETTINGS)

    @property
    def delay(self) -> float:
        return float(self.__config.get('Settings', 'delay'))

    @property
    def shooter_type(self) -> str:
        return self.__config.get('Settings', 'shooter_type')

    @property
    def point_type(self) -> str:
        return self.__config.get('Settings', 'point_type')

    def next_shooter_type(self) -> None:
        shooter_type = self.__config.get('Settings', 'shooter_type')
        if shooter_type == 'Me':
            self.__config.set('Settings', 'shooter_type', 'Ally')
        else:
            self.__config.set('Settings', 'shooter_type', 'Me')

        with open(CONFIG_PATH_SETTINGS, 'w') as f:
            self.__config.write(f)

    def next_point_type(self) -> None:
        shooter_type = self.__config.get('Settings', 'point_type')
        if shooter_type == 'Yellow':
            self.__config.set('Settings', 'point_type', 'Red')
        else:
            self.__config.set('Settings', 'point_type', 'Yellow')

        with open(CONFIG_PATH_SETTINGS, 'w') as f:
            self.__config.write(f)
