import logging
import os

from pet_shop import settings

logger = logging.getLogger(__name__)


def remove_image(path: str) -> bool:
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, f"{path}")
        os.remove(file_path)
        return True
    except Exception as ex:
        logger.debug(f"The image cannot be removed! ex:{ex}")
        return False
