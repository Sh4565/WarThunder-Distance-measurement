
import gettext
import configparser

from .main import CONFIG_PATH_SETTINGS


class SettingsConf:
    def __init__(self):
        self.lang = None
        self.__config = configparser.ConfigParser()
        self.__config.read(CONFIG_PATH_SETTINGS)

        gettext.bindtextdomain('cli', 'locales')
        gettext.textdomain('cli')

        self._translations = {
            'en': gettext.translation('cli', localedir='locales', languages=['en']),
            'ru': gettext.translation('cli', localedir='locales', languages=['ru']),
            'ua': gettext.translation('cli', localedir='locales', languages=['ua'])
        }

        self.set_language(self.__config.get('Settings', 'local'))

    def set_language(self, language: str) -> None:
        self.__config.set('Settings', 'local', language)
        translation = self._translations.get(language)
        if translation:
            translation.install()
            self.lang = translation.gettext
        else:
            raise ValueError(f"Unsupported language: {language}")

        with open(CONFIG_PATH_SETTINGS, 'w') as f:
            self.__config.write(f)

    @property
    def local(self) -> str:
        return self.__config.get('Settings', 'local')

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
