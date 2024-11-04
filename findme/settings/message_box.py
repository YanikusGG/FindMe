from dataclasses import dataclass
from typing import ClassVar, Self

from findme.utils import resolution


@dataclass
class MessageBoxSettings:
    """Настройки блока сообщений."""

    width: int
    height: int

    _percentage: ClassVar[float] = 20.0

    @classmethod
    def from_resolution(cls: type[Self]) -> "MessageBoxSettings":
        """Получить настройки, исходя из разрешения экрана."""
        width, height = resolution.get_shape()

        width *= cls._percentage / 100.0
        height *= cls._percentage / 100.0

        return MessageBoxSettings(int(width), int(height))
