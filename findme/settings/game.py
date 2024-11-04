from dataclasses import dataclass

from findme.enums.mode import Mode


@dataclass
class GameSettings:
    """Настройки игры."""

    title: str = "Find Me"
    mode: Mode = Mode.RANDOM
