
import configparser

from pathlib import Path
from .main import BASE_DIR


config = configparser.ConfigParser()

config.read(Path(BASE_DIR, 'config.cfg'))


if config.getint('Settings', 'who') == 1:
    WHO = 'Я'
elif config.getint('Settings', 'who') == 0:
    WHO = 'Союзник'

if config.getint('Settings', 'point') == 1:
    POINT = 'Желтая метка'
elif config.getint('Settings', 'point') == 0:
    POINT = 'Красная метка'
