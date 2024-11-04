from functools import cache

from screeninfo import get_monitors


@cache
def get_shape() -> tuple[int, int]:
    """Получить разрешение экрана."""
    if not (monitors := get_monitors()):
        detail = "Failed to get the screen resolution"
        raise RuntimeError(detail)

    for monitor in monitors:
        if monitor.is_primary:
            return (monitor.width, monitor.height)

    detail = "Failed to detect the primary monitor"
    raise RuntimeError(detail)
