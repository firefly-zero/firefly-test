from __future__ import annotations

from collections import Counter
from typing import Final, Iterator, Mapping, TYPE_CHECKING

from ._color import Color, PAT_TO_COLOR

if TYPE_CHECKING:
    from typing_extensions import Self

WIDTH = 240
"""Screen width in pixels.

This is the default width of Frame returned by Firefly.get_frame.
"""

HEIGHT = 160
"""Screen height in pixels.

This is the default height of Frame returned by Firefly.get_frame.
"""


_COLOR_TO_PAT: Final[Mapping[int, str]] = {
    v: k for k, v in PAT_TO_COLOR.items()
}


class Frame:
    __slots__ = ('_buf', '_width')
    _buf: list[int]
    _width: int

    def __init__(self, buf: list[int], *, width: int) -> None:
        self._buf = buf
        assert 0 <= width <= WIDTH
        assert 0 < len(buf) <= WIDTH * HEIGHT
        assert type(buf[0]) is int
        self._width = width

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return len(self._buf) // self._width

    def at(self, x: int, y: int | None = None) -> Color:
        """Get the color of the pixel with the given coordinates.

        Can accept either x and y or a flat single number index of the pixel
        in the frame buffer array.
        """
        if y is not None:
            assert 0 <= x < self.width
            assert 0 <= y < self.height
            x = y * self._width + x
        return Color(self._buf[x])

    def get_sub(
        self, *,
        x: int = 0,
        y: int = 0,
        width: int | None = None,
        height: int | None = None,
    ) -> Self:
        """Get a subregion of the frame.

        The region must be fully within the frame.
        """
        if width is None:
            width = self.width - x
        if height is None:
            height = self.height - y
        assert 0 <= x < self.width
        assert 0 <= y < self.height
        assert 0 <= width < self.width
        assert 0 <= height < self.height
        assert 0 <= x + width <= self.width
        assert 0 <= x + height <= self.height

        res_buf = []
        for line_no in range(y, y + height):
            start = line_no * self._width + x
            end = start + width
            line = self._buf[start:end]
            res_buf.extend(line)
        return type(self)(res_buf, width=width)

    def to_dict(self) -> dict[Color, int]:
        """Get the dict of how many pixels of each color the frame has.

        The dict contains only colors present on the screen.
        """
        return dict(self.to_counter())

    def to_set(self) -> set[Color]:
        """Get the set of all colors present on the frame.
        """
        return set(self.to_counter())

    def to_counter(self) -> Counter[Color]:
        """Get the count of pixels of each color on the frame.
        """
        return Counter(self)

    def __iter__(self) -> Iterator[Color]:
        """Iterate over all pixels in the frame.

        Iteration goes left-to-right and top-to-bottom,
        like scanlines in the old CRT displays or how you read English text.
        """
        return (Color(pixel) for pixel in self._buf)

    def __contains__(self, val: object) -> bool:
        if isinstance(val, int):
            assert 0x000000 <= val <= 0xFFFFFF
            return val in self._buf
        if isinstance(val, Color):
            return val in self.__iter__()
        t = type(val).__name__
        raise TypeError(f'Frame can contain only Color, not {t}')

    def __getitem__(self, i: int | tuple[int, int]) -> Color:
        if isinstance(i, tuple):
            x, y = i
            if x >= self._width:
                raise IndexError('x is out of range')
            i = y * self._width + x
        return Color(self._buf[i])

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            patterns = [p.strip() for p in other.splitlines()]
            patterns = [p for p in patterns if p]
            for i, pattern in enumerate(patterns):
                if not self._check_line(i, pattern):
                    return False
            return True
        if isinstance(other, type(self)):
            if self._width != other._width:
                raise TypeError('can compare only frames of the same width')
            return self._buf == other._buf
        return NotImplemented

    def __str__(self) -> str:
        """Represent the frame as a pattern.
        """
        res = ''
        for i in range(0, len(self._buf), self._width):
            raw_line = self._buf[i:i+self._width]
            line = ''.join(_COLOR_TO_PAT.get(c, '*') for c in raw_line)
            res += line + '\n'
        return res

    def __len__(self) -> int:
        return len(self._buf)

    def _check_line(self, i: int, pattern: str) -> bool:
        """Check if the given line matches the given pattern.

        The pattern can be shorter than the line.
        In that case, only the line prefix is checked.
        """
        pattern = ''.join(pattern.split())  # remove spaces
        assert 0 < len(pattern) <= self._width
        start = i * self._width
        end = start + self._width
        line = self._buf[start:end]
        return all(Color(act) == exp for act, exp in zip(line, pattern))
