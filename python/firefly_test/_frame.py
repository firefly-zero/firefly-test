from __future__ import annotations

from typing import Self

from ._color import Color

WIDTH = 240
HEIGHT = 160


class Frame:
    __slots__ = ('_buf', '_width')
    _buf: list[int]
    _width: int

    def __init__(self, buf: list[int], width: int) -> None:
        self._buf = buf
        self._width = width

    def at(self, x: int, y: int | None = None) -> Color:
        if y:
            assert 0 <= x < WIDTH
            assert 0 < y < HEIGHT
            x = y * self._width + x
        return Color(self._buf[x])

    def get_sub(
        self, *,
        x: int = 0,
        y: int = 0,
        width: int = WIDTH,
        height: int = HEIGHT,
    ) -> Self:
        assert 0 <= x < WIDTH
        assert 0 <= y < HEIGHT
        assert 0 <= width < WIDTH
        assert 0 <= height < HEIGHT
        assert 0 <= x + width < WIDTH
        assert 0 <= x + height < HEIGHT

        start = y * self._width + x
        size = self._width * height
        buf = self._buf[start:]
        buf = buf[:size]
        res_buf = []
        for i in range(0, len(buf), self._width):
            line = buf[i:i+width]
            res_buf.extend(line)
        return type(self)(buf, width=width)

    def __getitem__(self, i: int | tuple[int, int]) -> Color:
        if isinstance(i, tuple):
            x, y = i
            i = y * self._width + x
        return Color(self._buf[y])
