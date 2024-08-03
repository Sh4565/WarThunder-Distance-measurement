
from dataclasses import dataclass


@dataclass
class HSV:
    min: tuple = (None, None, None)
    max: tuple = (None, None, None)
