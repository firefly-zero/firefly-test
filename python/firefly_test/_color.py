from __future__ import annotations

from colorsys import rgb_to_hls, rgb_to_hsv, rgb_to_yiq
from typing import ClassVar, Final, Mapping


class Color:
    __slots__ = ('_raw',)
    _raw: int

    # Colors from the default color palette (SWEETIE 16)
    # https://lospec.com/palette-list/sweetie-16
    BLACK: ClassVar[Color]
    PURPLE: ClassVar[Color]
    RED: ClassVar[Color]
    ORANGE: ClassVar[Color]
    YELLOW: ClassVar[Color]
    LIGHT_GREEN: ClassVar[Color]
    GREEN: ClassVar[Color]
    DARK_GREEN: ClassVar[Color]
    DARK_BLUE: ClassVar[Color]
    BLUE: ClassVar[Color]
    LIGHT_BLUE: ClassVar[Color]
    CYAN: ClassVar[Color]
    WHITE: ClassVar[Color]
    LIGHT_GRAY: ClassVar[Color]
    GRAY: ClassVar[Color]
    DARK_GRAY: ClassVar[Color]

    # The extreme colors useful for debugging.
    TRUE_BLACK: ClassVar[Color]
    TRUE_WHITE: ClassVar[Color]
    TRUE_RED: ClassVar[Color]
    TRUE_GREEN: ClassVar[Color]
    TRUE_BLUE: ClassVar[Color]

    def __init__(self, raw: int) -> None:
        assert 0x000000 <= raw <= 0xFFFFFF
        self._raw = raw

    @property
    def r(self) -> int:
        return (self._raw >> 16) & 0xFF

    @property
    def g(self) -> int:
        return (self._raw >> 8) & 0xFF

    @property
    def b(self) -> int:
        return self._raw & 0xFF

    @property
    def rgb(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)

    @property
    def hls(self) -> tuple[float, float, float]:
        """Color HLS representation: Hue, Lightness, and Saturation.

        Each value is in the [0.0..1.0] range.

        https://en.wikipedia.org/wiki/HSL_and_HSV
        """
        return rgb_to_hls(self.r / 255, self.g / 255, self.b / 255)

    @property
    def hsv(self) -> tuple[float, float, float]:
        """Color HSV representation: Hue, Saturation, and Value (Brightness).

        Each value is in the [0.0..1.0] range.

        https://en.wikipedia.org/wiki/HSL_and_HSV
        """
        return rgb_to_hsv(self.r / 255, self.g / 255, self.b / 255)

    @property
    def yiq(self) -> tuple[float, float, float]:
        """Color YIQ representation.

        https://en.wikipedia.org/wiki/YIQ
        """
        return rgb_to_yiq(self.r / 255, self.g / 255, self.b / 255)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            if other == '.':
                return True
            color = PAT_TO_COLOR[other]
            return self._raw == color
        if isinstance(other, Color):
            return self._raw == other._raw
        if isinstance(other, int):
            assert 0x000000 <= other <= 0xFFFFFF
            return self._raw == other
        return NotImplemented

    def __repr__(self) -> str:
        return f'{type(self).__name__}(0x{self._raw:06X})'

    def __str__(self) -> str:
        return f'#{self._raw:06X}'

    def __int__(self) -> int:
        return self._raw

    def __hash__(self) -> int:
        return hash(self._raw)


# Color instances can be initialized only after Color class is created.
Color.BLACK = Color(0x1A1C2C)
Color.PURPLE = Color(0x5D275D)
Color.RED = Color(0xB13E53)
Color.ORANGE = Color(0xEF7D57)
Color.YELLOW = Color(0xFFCD75)
Color.LIGHT_GREEN = Color(0xA7F070)
Color.GREEN = Color(0x38B764)
Color.DARK_GREEN = Color(0x257179)
Color.DARK_BLUE = Color(0x29366F)
Color.BLUE = Color(0x3B5DC9)
Color.LIGHT_BLUE = Color(0x41A6F6)
Color.CYAN = Color(0x73EFF7)
Color.WHITE = Color(0xF4F4F4)
Color.LIGHT_GRAY = Color(0x94B0C2)
Color.GRAY = Color(0x566C86)
Color.DARK_GRAY = Color(0x333C57)

Color.TRUE_BLACK = Color(0x000000)
Color.TRUE_WHITE = Color(0xFFFFFF)
Color.TRUE_RED = Color(0xFF0000)
Color.TRUE_GREEN = Color(0x00FF00)
Color.TRUE_BLUE = Color(0x0000FF)

PAT_TO_COLOR: Final[Mapping[str, int]] = {
    'K': int(Color.BLACK),
    'P': int(Color.PURPLE),
    'R': int(Color.RED),
    'O': int(Color.ORANGE),
    'Y': int(Color.YELLOW),
    # LIGHT_GREEN
    'G': int(Color.GREEN),
    # DARK_GREEN
    # DARK_BLUE
    'B': int(Color.BLUE),
    # LIGHT_BLUE
    'C': int(Color.CYAN),
    'W': int(Color.WHITE),
    # LIGHT_GRAY
    # GRAY
    # DARK_GRAY
}
