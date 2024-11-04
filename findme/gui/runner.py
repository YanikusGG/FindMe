from dataclasses import dataclass, field
from typing import Self

import arcade

from findme.gui.game import FindMe
from findme.settings.game import GameSettings
from findme.settings.message_box import MessageBoxSettings
from findme.settings.screen import ScreenSettings


@dataclass
class Runner:
    """Инициатор игры."""

    game_settings: "GameSettings" = field(default_factory=GameSettings)
    message_box_settings: "MessageBoxSettings" = field(default_factory=MessageBoxSettings.from_resolution)
    screen_settings: "ScreenSettings" = field(default_factory=ScreenSettings.from_resolution)

    def run(self: Self) -> None:
        """Запустить игру."""
        game = FindMe(self.game_settings, self.message_box_settings, self.screen_settings)
        game.setup()
        arcade.run()
