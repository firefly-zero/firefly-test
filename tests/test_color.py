from firefly_test import Color


def test_eq() -> None:
    assert Color.TRUE_BLACK == 0x000000
    assert 0x000000 == Color.TRUE_BLACK  # noqa: SIM300
    assert Color.TRUE_BLACK != 0x000010
    assert 0x000010 != Color.TRUE_BLACK  # noqa: SIM300

    assert Color.BLACK == 'K'
    assert Color.BLACK != 'B'
    assert Color.BLACK == '.'

    assert Color.BLACK == Color.BLACK
    assert Color.TRUE_BLACK == Color.from_rgb24(0x000000)  # noqa: SIM300
    assert Color.BLACK != Color.TRUE_BLACK

    assert Color.BLACK != []
    assert Color.BLACK != ()
    assert Color.BLACK != 1.3


def test_rgb() -> None:
    c = Color.TRUE_RED
    assert 248 <= c.r <= 255
    assert c.g == 0x00
    assert c.b == 0x00
    assert 0.97 <= c.rgb[0] <= 1.00
    assert c.rgb[1] == 0
    assert c.rgb[2] == 0

    c = Color.TRUE_GREEN
    assert c.r == 0x00
    assert 252 <= c.g <= 255
    assert c.b == 0x00
    assert c.rgb[0] == 0
    assert 0.97 <= c.rgb[1] <= 1.00
    assert c.rgb[2] == 0

    c = Color.TRUE_BLUE
    assert c.r == 0x00
    assert c.g == 0x00
    assert 248 <= c.b <= 255
    assert c.rgb[0] == 0
    assert c.rgb[1] == 0
    assert 0.97 <= c.rgb[2] <= 1.00


def test_colorsys() -> None:
    c = Color.TRUE_WHITE
    assert c.hls == (0, 1, 0)
    assert c.hsv == (0, 0, 1)

    assert 0.9999 < c.yiq[0] < 1.0
    assert 0 < c.yiq[1] < 0.00001
    assert 0 < c.yiq[2] < 0.00001


def test_str() -> None:
    assert str(Color.TRUE_RED) == '#FF0000'
    assert str(Color.TRUE_GREEN) == '#00FF00'
    assert str(Color.TRUE_BLUE) == '#0000FF'
    assert str(Color.TRUE_BLACK) == '#000000'


def test_repr() -> None:
    assert repr(Color.from_rgb24(0x1289CD)) == 'Color(0x1289CD)'

    assert repr(Color.TRUE_RED) == 'Color.TRUE_RED'
    assert repr(Color.TRUE_GREEN) == 'Color.TRUE_GREEN'
    assert repr(Color.TRUE_BLUE) == 'Color.TRUE_BLUE'
    assert repr(Color.TRUE_BLACK) == 'Color.TRUE_BLACK'
    assert repr(Color.TRUE_WHITE) == 'Color.TRUE_WHITE'

    assert repr(Color.BLACK) == 'Color.BLACK'
    assert repr(Color.PURPLE) == 'Color.PURPLE'
    assert repr(Color.RED) == 'Color.RED'
    assert repr(Color.ORANGE) == 'Color.ORANGE'
    assert repr(Color.YELLOW) == 'Color.YELLOW'
    assert repr(Color.LIGHT_GREEN) == 'Color.LIGHT_GREEN'
    assert repr(Color.GREEN) == 'Color.GREEN'
    assert repr(Color.DARK_GREEN) == 'Color.DARK_GREEN'
    assert repr(Color.DARK_BLUE) == 'Color.DARK_BLUE'
    assert repr(Color.BLUE) == 'Color.BLUE'
    assert repr(Color.LIGHT_BLUE) == 'Color.LIGHT_BLUE'
    assert repr(Color.CYAN) == 'Color.CYAN'
    assert repr(Color.WHITE) == 'Color.WHITE'
    assert repr(Color.LIGHT_GRAY) == 'Color.LIGHT_GRAY'
    assert repr(Color.GRAY) == 'Color.GRAY'
    assert repr(Color.DARK_GRAY) == 'Color.DARK_GRAY'
