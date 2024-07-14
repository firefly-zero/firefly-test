from __future__ import annotations

from colorsys import rgb_to_hls, rgb_to_hsv, rgb_to_yiq
from enum import Enum
from typing import Final, Mapping


class DefaultColor(Enum):
    """Enum of colors in the default palette.

    https://lospec.com/palette-list/sweetie-16
    """
    BLACK = 0x1A1C2C
    PURPLE = 0x5D275D
    RED = 0xB13E53
    ORANGE = 0xEF7D57
    YELLOW = 0xFFCD75
    LIGHT_GREEN = 0xA7F070
    GREEN = 0x38B764
    DARK_GREEN = 0x257179
    DARK_BLUE = 0x29366F
    BLUE = 0x3B5DC9
    LIGHT_BLUE = 0x41A6F6
    CYAN = 0x73EFF7
    WHITE = 0xF4F4F4
    LIGHT_GRAY = 0x94B0C2
    GRAY = 0x566C86
    DARK_GRAY = 0x333C57


_PAT_TO_COLOR: Final[Mapping[str, DefaultColor]] = {
    'K': DefaultColor.BLACK,
    'P': DefaultColor.PURPLE,
    'R': DefaultColor.RED,
    'O': DefaultColor.ORANGE,
    'Y': DefaultColor.YELLOW,
    # LIGHT_GREEN
    'G': DefaultColor.GREEN,
    # DARK_GREEN
    # DARK_BLUE
    'B': DefaultColor.BLUE,
    # LIGHT_BLUE
    'C': DefaultColor.CYAN,
    'W': DefaultColor.WHITE,
    # LIGHT_GRAY
    # GRAY
    # DARK_GRAY
}


class Color:
    __slots__ = ('_raw',)
    _raw: int

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
        return rgb_to_hls(self.r / 255, self.g / 255, self.b / 255)

    @property
    def hsv(self) -> tuple[float, float, float]:
        return rgb_to_hsv(self.r / 255, self.g / 255, self.b / 255)

    @property
    def yiq(self) -> tuple[float, float, float]:
        return rgb_to_yiq(self.r / 255, self.g / 255, self.b / 255)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            if other == '.':
                return True
            color = _PAT_TO_COLOR[other]
            return self._raw == color.value
        if isinstance(other, DefaultColor):
            return self._raw == other.value
        if isinstance(other, Color):
            return self._raw == other._raw
        if isinstance(other, int):
            assert 0x000000 <= other <= 0xFFFFFF
            return self._raw == other
        return NotImplemented

    def __repr__(self) -> str:
        return f'{type(self).__name__}(0x{self._raw:X})'

    def __str__(self) -> str:
        return f'#{self._raw:X}'
