from __future__ import annotations

from collections import Counter
from typing import Final, Iterator, Mapping, TYPE_CHECKING

from ._color import Color, DefaultColor

if TYPE_CHECKING:
    from typing import Self

WIDTH = 240
HEIGHT = 160


_COLOR_TO_PAT: Final[Mapping[int, str]] = {
    DefaultColor.BLACK.value: 'K',
    DefaultColor.PURPLE.value: 'P',
    DefaultColor.RED.value: 'R',
    DefaultColor.ORANGE.value: 'O',
    DefaultColor.YELLOW.value: 'Y',
    # LIGHT_GREEN
    DefaultColor.GREEN.value: 'G',
    # DARK_GREEN
    # DARK_BLUE
    DefaultColor.BLUE.value: 'B',
    # LIGHT_BLUE
    DefaultColor.CYAN.value: 'C',
    DefaultColor.WHITE.value: 'W',
    # LIGHT_GRAY
    # GRAY
    # DARK_GRAY
}


class Frame:
    __slots__ = ('_buf', '_width')
    _buf: list[int]
    _width: int

    def __init__(self, buf: list[int], width: int) -> None:
        self._buf = buf
        assert 0 <= width <= WIDTH
        assert 0 < len(buf) <= WIDTH * HEIGHT
        self._width = width

    @property
    def width(self) -> int:
        return self.width

    @property
    def height(self) -> int:
        return len(self._buf) // self.width

    def at(self, x: int, y: int | None = None) -> Color:
        if y:
            assert 0 <= x < self.width
            assert 0 < y < self.height
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
        """
        if width is None:
            width = self.width - x
        if height is None:
            height = self.height - y
        assert 0 <= x < self.width
        assert 0 <= y < self.height
        assert 0 <= width < self.width
        assert 0 <= height < self.height
        assert 0 <= x + width < self.width
        assert 0 <= x + height < self.height

        start = y * self._width + x
        size = self._width * height
        buf = self._buf[start:]
        buf = buf[:size]
        res_buf = []
        for i in range(0, len(buf), self._width):
            line = buf[i:i+width]
            res_buf.extend(line)
        return type(self)(buf, width=width)

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

    def __contains__(self, val: DefaultColor | Color | int | str) -> bool:
        if isinstance(val, int):
            assert 0x000000 <= val <= 0xFFFFFF
            return val in self._buf
        if isinstance(val, Color):
            return val in self
        if isinstance(val, (str, DefaultColor)):
            return any(c == val for c in self)
        raise TypeError

    def __getitem__(self, i: int | tuple[int, int]) -> Color:
        if isinstance(i, tuple):
            x, y = i
            i = y * self._width + x
        return Color(self._buf[y])

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            for i, pattern in enumerate(other.splitlines()):
                if not self._check_line(i, pattern):
                    return False
            return True
        return NotImplemented

    def __repr__(self) -> str:
        """Make a repr that will give a nice diff in pytest.
        """
        res = ''
        for i in range(0, len(self._buf), self._width):
            raw_line = self._buf[i:i+self._width]
            line = ''.join(_COLOR_TO_PAT.get(c, '*') for c in raw_line)
            res += line + '\n'
        return res

    def _check_line(self, i: int, pattern: str) -> bool:
        """Check if the given line matches the given pattern.

        The pattern can be shorter than the line.
        In that case, only the line prefix is checked.
        """
        pattern = ''.join(pattern.split())  # remove spaces
        assert 0 < len(pattern) <= self._width
        line = self._buf[i:i+self._width]
        return all(Color(act) == exp for act, exp in zip(line, pattern))
