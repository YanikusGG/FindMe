import os

from pathlib import Path
from tempfile import mkstemp

from PIL import Image


def crop(source: Path, x0: int, y0: int, x1: int, y1: int) -> Path:
    """Обрезать изображение."""
    with Image.open(source) as image:
        box = (x0, y0, x1, y1)
        cropped = image.crop(box)

    fd, path = mkstemp(suffix=source.suffix)
    os.close(fd)

    cropped.save(path)
    return Path(path)


def get_shape(source: Path) -> tuple[int, int]:
    """Получить размеры изображения."""
    with Image.open(source) as image:
        return (image.width, image.height)
