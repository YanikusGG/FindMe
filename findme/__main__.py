from contextlib import suppress

from findme.gui.runner import Runner

from pyglet.image.atlas import AllocatorException


def main() -> None:
    """Запустить игру."""
    runner = Runner()
    runner.run()


if __name__ == "__main__":
    while True:
        with suppress(Exception):
            main()
