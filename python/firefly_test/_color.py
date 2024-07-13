from __future__ import annotations
from enum import Enum


class DefaultColor(Enum):
    BLACK = 0x1A1C2C        # K
    PURPLE = 0x5D275D       # P
    RED = 0xB13E53          # R
    ORANGE = 0xEF7D57       # O
    YELLOW = 0xFFCD75       # Y
    LIGHT_GREEN = 0xA7F070
    GREEN = 0x38B764        # G
    DARK_GREEN = 0x257179
    DARK_BLUE = 0x29366F
    BLUE = 0x3B5DC9         # B
    LIGHT_BLUE = 0x41A6F6
    CYAN = 0x73EFF7         # C
    WHITE = 0xF4F4F4        # W
    LIGHT_GRAY = 0x94B0C2
    GRAY = 0x566C86
    DARK_GRAY = 0x333C57


class Color:
    __slots__ = ('_raw',)
    _raw: int

    def __init__(self, raw: int) -> None:
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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Color):
            return self._raw == other._raw
        if isinstance(other, int):
            return self._raw == other
        return NotImplemented
