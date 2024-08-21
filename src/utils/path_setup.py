
import sys
from pathlib import Path


def setup_paths():
    src_path = Path(__file__).resolve().parent.parent
    sys.path.append(str(src_path))
