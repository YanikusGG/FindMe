from pathlib import Path
from secrets import randbelow
from datetime import datetime
from typing import TYPE_CHECKING, Self

from arcade import draw_lrwh_rectangle_textured, draw_text
from arcade.application import Window
from arcade.gui.constructs import UIMessageBox
from arcade.gui.widgets import UITextureButton
from arcade.gui.ui_manager import UIManager
from arcade.texture import Texture, load_texture
import arcade

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
            resizable=True,
        )

        self._game_settings: GameSettings = game_settings
        self._message_box_settings: MessageBoxSettings = message_box_settings
        self._screen_settings: ScreenSettings = screen_settings
        self._level = 0
        self._menu_id = 1

        self._sprite: Texture
        self._box: tuple[float, float, float, float] = None

        self.manager = UIManager(self)
        self.manager.enable()

        self.open_main_menu()

    def setup(self: Self, extra: any = None) -> None:
        """Перезагрузить игру."""
        self.clear()

        path_to_background = Randomizer.get_background()
        self.background = load_texture(path_to_background)
        self._level_start = None
        self.manager.draw()

    def open_main_menu(self: Self):
        self._menu_id = 1
        self._level_start = None
        v_box = arcade.gui.UIBoxLayout()

        start_btn = arcade.gui.UIFlatButton(text="Start Game", width=200)
        v_box.add(start_btn.with_space_around(bottom=20))

        @start_btn.event("on_click")
        def on_click_start(event):
            self.run_level()
            self._menu_id = 0

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=v_box)
        )

    def run_level(self: Self, extra: any = None) -> None:
        self.manager.clear()
        path_to_background = Randomizer.get_background()
        self.background = load_texture(path_to_background)
        path_to_object = Randomizer.get_object()
        self.object = load_texture(path_to_object)
        self._box = self._get_crop_box(path_to_object)
        self._level_start = datetime.now()
        self._level += 1
        self.manager.draw()

    def draw_main_menu(self: Self) -> None:
        draw_lrwh_rectangle_textured(
            bottom_left_x=0,
            bottom_left_y=0,
            width=self.width,
            height=self.height,
            texture=self.background,
        )
        arcade.draw_lrtb_rectangle_filled(
            left=0.4 * self.width,
            right=0.6 * self.width,
            bottom = 0.7 * self.height,
            top=0.8 * self.height,
            color=arcade.color.WHITE,
        )
        draw_text(
            "FindME",
            0.4 * self.width, 0.73 * self.height,
            arcade.color.BLACK,
            30,
            width=0.2 * self.width,
            align="center",
            font_name="Comic Sans MS",
        )
        self.manager.draw()
        return

    def draw_game(self: Self) -> None:
        draw_lrwh_rectangle_textured(
            bottom_left_x=0,
            bottom_left_y=0,
            width=self.width,
            height=self.height,
            texture=self.background,
        )

        if self._box is not None:
            x0, y0, x1, y1 = self._box
            x0 = x0 * self.width
            y0 = y0 * self.height
            x1 = x1 * self.width
            y1 = y1 * self.height
            draw_lrwh_rectangle_textured(
                bottom_left_x=x0,
                bottom_left_y=y0,
                width=x1-x0,
                height=y1-y0,
                texture=self.object,
            )

        now = datetime.now()
        if self._level_start:
            draw_text(
                "Timer: {:02d}:{:02d}".format(round((now - self._level_start).total_seconds())//60, round((now - self._level_start).total_seconds())%60),
                50, 50,
                arcade.color.WHITE,
                20,
                # width=450,
                align="left"
            )
            draw_text(
                "Level #{:d}".format(self._level),
                0.8 * self.width, 50,
                arcade.color.WHITE,
                20,
                # width=450,
                align="left"
            )

        self.manager.draw()

    def on_draw(self: Self) -> None:
        """Отобразить экран."""
        self.clear()

        if self._menu_id == 1:
            self.draw_main_menu()
        elif self._menu_id == 0:
            self.draw_game()


    def on_mouse_press(self: Self, x: int, y: int, _button: int, _modifiers: int) -> None:
        """Триггер на нажатия мыши."""
        if self._menu_id == 0:
            if self._box is None:
                return
            x0, y0, x1, y1 = self._box
            x0 = x0 * self.width
            y0 = y0 * self.height
            x1 = x1 * self.width
            y1 = y1 * self.height

            if not ((x0 <= x <= x1) and (y0 <= y <= y1)):
                return

            self._level_stop = datetime.now()
            widget = UIMessageBox(
                width=self._message_box_settings.width,
                height=self._message_box_settings.height,
                message_text=Message.VICTORY + "\n" + str(round((self._level_stop - self._level_start).total_seconds(), 2)) + " seconds!",
                buttons=[Message.HOORAY],
                callback=self.run_level,
            )

            self.manager.add(widget)
        elif self._menu_id == 1:
            """Main menu logic"""

    def on_key_press(self: Self, symbol: int, modifiers: int) -> None:
        if symbol == 65307:
            self.open_main_menu()

    def _get_crop_box(self: Self, image: Path) -> tuple[float, float, float, float]:
        """Получить параметры обрезки заднего фона."""
        width, height = photoshop.get_shape(image)

        if self._game_settings.mode == Mode.RANDOM:
            const = 15

            x0, y0 = randbelow(self.width - width), randbelow(self.height - height)
            dx, dy = randbelow(const) + const, randbelow(const) + const
            return (x0 / self.width, y0 / self.height, (x0 + dx) / self.width, (y0 + dy)/self.height)

        detail = "This code is unreachable"
        raise RuntimeError(detail)
