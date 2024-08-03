
from pathlib import Path
from loguru import logger

from .main import BASE_DIR


logger.add(
    Path(BASE_DIR, 'errors.log'),
    format="[{time:YYYY-MM-DD at HH:mm:ss}]: {level} ({file}:{line}) - {message}",
    rotation='40 MB',
    retention='7 days',
    level="WARNING"
)
