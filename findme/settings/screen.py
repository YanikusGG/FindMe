from dataclasses import dataclass

from findme.utils import resolution


@dataclass
class ScreenSettings:
    """Настройки экрана."""

    width: int
    height: int

    @staticmethod
    def from_resolution() -> "ScreenSettings":
        """Получить настройки, исходя из разрешения экрана."""
        width, height = resolution.get_shape()
        return ScreenSettings(width, height)
