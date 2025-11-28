from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing_extensions import Self


class Pad:
    __slots__ = ('_x', '_y')
    _x: int
    _y: int

    def __init__(self, x: int, y: int) -> None:
        assert -1000 <= x <= 1000
        assert -1000 <= y <= 1000
        self._x = x
        self._y = y


class Input:
    _pad: Pad
    _buttons: int

    def __init__(
        self,
        pad: Pad | None = None,
        *,
        s: bool = False,
        e: bool = False,
        w: bool = False,
        n: bool = False,
        menu: bool = False,
    ) -> None:
        if pad is None:
            pad = Pad(x=0xFF, y=0xFF)
        self._pad = pad
        buttons = 0
        if s:
            buttons |= 0b1
        if e:
            buttons |= 0b10
        if w:
            buttons |= 0b100
        if n:
            buttons |= 0b1000
        if menu:
            buttons |= 0b10000
        self._buttons = buttons

    def __or__(self, other: Self) -> Self:
        pad = self._pad
        if pad._x == 0xFF:
            pad = other._pad
        res = type(self)(pad)
        res._buttons = self._buttons | other._buttons
        return res
