
import os

from pathlib import Path


if os.path.isfile(Path(__file__).resolve()):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
