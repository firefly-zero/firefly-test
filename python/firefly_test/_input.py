from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing_extensions import Self


class Pad:
    __slots__ = ('_x', '_y')
    _x: int
    _y: int

    def __init__(self, x: int, y: int) -> None:
        assert 0 <= x <= 1000
        assert 0 <= y <= 1000
        self._x = x
        self._y = y


class Input:
    _pad: Pad | None
    _buttons: int

    def __init__(
        self,
        pad: Pad | None = None,
        *,
        a: bool = False,
        b: bool = False,
        x: bool = False,
        y: bool = False,
        menu: bool = False,
    ) -> None:
        self._pad = pad
        buttons = 0
        if a:
            buttons |= 0b1
        if b:
            buttons |= 0b10
        if x:
            buttons |= 0b100
        if y:
            buttons |= 0b1000
        if menu:
            buttons |= 0b10000
        self._buttons = buttons

    def __or__(self, other: Self) -> Self:
        res = type(self)(self._pad or other._pad)
        res._buttons = self._buttons | other._buttons
        return res
