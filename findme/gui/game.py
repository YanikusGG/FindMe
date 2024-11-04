from pathlib import Path
from secrets import randbelow
from typing import TYPE_CHECKING, Self

from arcade import draw_lrwh_rectangle_textured
from arcade.application import Window
from arcade.gui.constructs import UIMessageBox
from arcade.gui.widgets import UITextureButton
from arcade.gui.ui_manager import UIManager
from arcade.texture import Texture, load_texture

from findme.enums.message import Message
from findme.enums.mode import Mode
from findme.gui.randomizer import Randomizer
from findme.utils import photoshop


if TYPE_CHECKING:
    from findme.settings.game import GameSettings
    from findme.settings.message_box import MessageBoxSettings
    from findme.settings.screen import ScreenSettings


class FindMe(Window):
    """Игра `FindMe`."""

    def __init__(
        self: Self,
        game_settings: "GameSettings",
        message_box_settings: "MessageBoxSettings",
        screen_settings: "ScreenSettings",
    ) -> None:
        """Инициализровать объект."""
        super().__init__(
            width=screen_settings.width,
            height=screen_settings.height,
            title=game_settings.title,
        )

        self._game_settings: GameSettings = game_settings
        self._message_box_settings: MessageBoxSettings = message_box_settings
        self._screen_settings: ScreenSettings = screen_settings

        self._sprite: Texture
        self._box: tuple[int, int, int, int] = ()

        self.manager = UIManager(self)
        self.manager.enable()

    def setup(self: Self) -> None:
        """Перезагрузить игру."""
        self.clear()

        path_to_background = Randomizer.get_background()
        self.background = load_texture(path_to_background)

        self._box = self._get_crop_box(path_to_background)
        path_to_sprite = photoshop.crop(path_to_background, *self._box)

        widget = UITextureButton(
            texture=load_texture(path_to_sprite),
            text=Message.FIND,
        )

        widget.on_click = lambda _: self.manager.remove(widget)
        widget = widget.with_border()

        widget.center_on_screen()

        self.manager.add(widget)
        self.manager.draw()

    def on_draw(self: Self) -> None:
        """Отобразить экран."""
        self.clear()

        draw_lrwh_rectangle_textured(
            bottom_left_x=0,
            bottom_left_y=0,
            width=self._screen_settings.width,
            height=self._screen_settings.height,
            texture=self.background,
        )

        self.manager.draw()

    def on_mouse_press(self: Self, x: int, y: int, _button: int, _modifiers: int) -> None:
        """Триггер на нажатия мыши."""
        x0, y0, x1, y1 = self._box

        # Для `arcade` ордината убывает сверху вниз
        y = self._screen_settings.height - y

        if not ((x0 <= x <= x1) and (y0 <= y <= y1)):
            return

        widget = UIMessageBox(
            width=self._message_box_settings.width,
            height=self._message_box_settings.height,
            message_text=Message.VICTORY,
            buttons=[Message.HOORAY],
        )

        self.manager.add(widget)

    def _get_crop_box(self: Self, image: Path) -> tuple[int, int, int, int]:
        """Получить параметры обрезки заднего фона."""
        width, height = photoshop.get_shape(image)

        if self._game_settings.mode == Mode.RANDOM:
            x0, y0 = randbelow(width), randbelow(height)
            dx, dy = randbelow(width - x0), randbelow(height - y0)
            return (x0, y0, x0 + dx, y0 + dy)

        detail = "This code is unreachable"
        raise RuntimeError(detail)
