from __future__ import annotations

from colorsys import rgb_to_hls, rgb_to_hsv, rgb_to_yiq
from typing import ClassVar, Final, Mapping


class Color:
    """An RGB color of a pixel on the Frame.
    """
    __slots__ = ('_raw',)
    _raw: int

    # Colors from the default color palette (SWEETIE 16)
    # https://lospec.com/palette-list/sweetie-16
    #
    # It could be an enum but enums work better when there is a well-known
    # in advance list of possible values.

    BLACK: ClassVar[Color]
    """The black color from the default palette (SWEETIE-16): #1A1C2C.
    """

    PURPLE: ClassVar[Color]
    """The purple color from the default palette (SWEETIE-16): #5D275D.
    """

    RED: ClassVar[Color]
    """The red color from the default palette (SWEETIE-16): #B13E53.
    """

    ORANGE: ClassVar[Color]
    """The orange color from the default palette (SWEETIE-16): #EF7D57.
    """

    YELLOW: ClassVar[Color]
    """The yellow color from the default palette (SWEETIE-16): #FFCD75.
    """

    LIGHT_GREEN: ClassVar[Color]
    """The light green color from the default palette (SWEETIE-16): #A7F070.
    """

    GREEN: ClassVar[Color]
    """The green color from the default palette (SWEETIE-16): #38B764.
    """

    DARK_GREEN: ClassVar[Color]
    """The dark green color from the default palette (SWEETIE-16): #257179.
    """

    DARK_BLUE: ClassVar[Color]
    """The dark blue color from the default palette (SWEETIE-16): #29366F.
    """

    BLUE: ClassVar[Color]
    """The blue color from the default palette (SWEETIE-16): #3B5DC9.
    """

    LIGHT_BLUE: ClassVar[Color]
    """The light blue color from the default palette (SWEETIE-16): #41A6F6.
    """

    CYAN: ClassVar[Color]
    """The cyan color from the default palette (SWEETIE-16): #73EFF7.
    """

    WHITE: ClassVar[Color]
    """The white color from the default palette (SWEETIE-16): #F4F4F4.
    """

    LIGHT_GRAY: ClassVar[Color]
    """The light gray color from the default palette (SWEETIE-16): #94B0C2.
    """

    GRAY: ClassVar[Color]
    """The gray color from the default palette (SWEETIE-16): #566C86.
    """

    DARK_GRAY: ClassVar[Color]
    """The dark gray color from the default palette (SWEETIE-16): #333C57.
    """

    # The extreme colors useful for debugging.
    TRUE_BLACK: ClassVar[Color]
    """Purely black color: #000000.
    """

    TRUE_WHITE: ClassVar[Color]
    """Purely white color: #FFFFFF.
    """

    TRUE_RED: ClassVar[Color]
    """Purely red color: #FF0000.
    """

    TRUE_GREEN: ClassVar[Color]
    """Purely green color: #00FF00.
    """

    TRUE_BLUE: ClassVar[Color]
    """Purely blue color: #0000FF.
    """

    def __init__(self, raw: int) -> None:
        assert 0x000000 <= raw <= 0xFFFFFF
        self._raw = raw

    @property
    def r(self) -> int:
        """The red component of the RGB color representation.

        A value from from 0 (no red) to 255 (as red as it gets).
        """
        return (self._raw >> 16) & 0xFF

    @property
    def g(self) -> int:
        """The green component of the RGB color representation.

        A value from from 0 (no green) to 255 (as green as it gets).
        """
        return (self._raw >> 8) & 0xFF

    @property
    def b(self) -> int:
        """The blue component of the RGB color representation.

        A value from from 0 (no blue) to 255 (as blue as it gets).
        """
        return self._raw & 0xFF

    @property
    def rgb(self) -> tuple[float, float, float]:
        """Color RGB representation: Reg, Green, and Blue.

        Each value is in the [0.0..1.0] range.

        https://en.wikipedia.org/wiki/RGB_color_model
        """
        return (self.r / 255, self.g / 255, self.b / 255)

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
        try:
            return _COLOR_TO_REPR[self._raw]
        except AttributeError:  # pragma: no cover
            # Partially initialized class, no value is set yet.
            # Might be reached if there is a failure in Color.__init__
            # and pytest includes repr in the error report.
            return f'{type(self).__name__}(???)'
        except KeyError:
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
    'g': int(Color.LIGHT_GREEN),
    'G': int(Color.GREEN),
    'D': int(Color.DARK_GREEN),
    'd': int(Color.DARK_BLUE),
    'B': int(Color.BLUE),
    'b': int(Color.LIGHT_BLUE),
    'C': int(Color.CYAN),
    'W': int(Color.WHITE),
    '◔': int(Color.LIGHT_GRAY),
    '◑': int(Color.GRAY),
    '◕': int(Color.DARK_GRAY),

    # For completeness with gray representations.
    # Experimental. In dark theme, white looks black and black looks white.
    '○': int(Color.WHITE),
    '●': int(Color.BLACK),

    # Experimental. Emojis show actual colors but they are also interpreted
    # by many terminals as 2 characters which makes the diff misaligned.
    '🖤': int(Color.BLACK),     # ◾
    '💜': int(Color.PURPLE),    # 🟪
    '♥️': int(Color.RED),       # 🟥
    '🧡': int(Color.ORANGE),    # 🟧
    '💛': int(Color.YELLOW),    # 🟨
    '💚': int(Color.GREEN),     # 🟩
    '💙': int(Color.BLUE),      # 🟦
    '🤍': int(Color.WHITE),     # ◽
    '🩶': int(Color.GRAY),
}

_COLOR_TO_REPR: Final[Mapping[int, str]] = {
    Color.BLACK._raw: 'Color.BLACK',
    Color.PURPLE._raw: 'Color.PURPLE',
    Color.RED._raw: 'Color.RED',
    Color.ORANGE._raw: 'Color.ORANGE',
    Color.YELLOW._raw: 'Color.YELLOW',
    Color.LIGHT_GREEN._raw: 'Color.LIGHT_GREEN',
    Color.GREEN._raw: 'Color.GREEN',
    Color.DARK_GREEN._raw: 'Color.DARK_GREEN',
    Color.DARK_BLUE._raw: 'Color.DARK_BLUE',
    Color.BLUE._raw: 'Color.BLUE',
    Color.LIGHT_BLUE._raw: 'Color.LIGHT_BLUE',
    Color.CYAN._raw: 'Color.CYAN',
    Color.WHITE._raw: 'Color.WHITE',
    Color.LIGHT_GRAY._raw: 'Color.LIGHT_GRAY',
    Color.GRAY._raw: 'Color.GRAY',
    Color.DARK_GRAY._raw: 'Color.DARK_GRAY',
    Color.TRUE_BLACK._raw: 'Color.TRUE_BLACK',
    Color.TRUE_WHITE._raw: 'Color.TRUE_WHITE',
    Color.TRUE_RED._raw: 'Color.TRUE_RED',
    Color.TRUE_GREEN._raw: 'Color.TRUE_GREEN',
    Color.TRUE_BLUE._raw: 'Color.TRUE_BLUE',
}
