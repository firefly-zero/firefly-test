from firefly_test import Color


def test_eq() -> None:
    assert Color.TRUE_BLACK == 0x000000
    assert 0x000000 == Color.TRUE_BLACK  # noqa: SIM300
    assert Color.TRUE_BLACK != 0x000001
    assert 0x000001 != Color.TRUE_BLACK  # noqa: SIM300

    assert Color.BLACK == 'K'
    assert Color.BLACK != 'B'
    assert Color.BLACK == '.'

    assert Color.BLACK == Color.BLACK
    assert Color.TRUE_BLACK == Color(0x000000)  # noqa: SIM300
    assert Color.BLACK != Color.TRUE_BLACK

    assert Color.BLACK != []
    assert Color.BLACK != ()
    assert Color.BLACK != 1.3


def test_rgb() -> None:
    c = Color.TRUE_RED
    assert c.r == 0xFF
    assert c.g == 0x00
    assert c.b == 0x00
    assert c.rgb == (0xFF, 0x00, 0x00)

    c = Color.TRUE_GREEN
    assert c.r == 0x00
    assert c.g == 0xFF
    assert c.b == 0x00
    assert c.rgb == (0x00, 0xFF, 0x00)

    c = Color.TRUE_BLUE
    assert c.r == 0x00
    assert c.g == 0x00
    assert c.b == 0xFF
    assert c.rgb == (0x00, 0x00, 0xFF)


def test_str() -> None:
    assert str(Color.TRUE_RED) == '#FF0000'
    assert str(Color.TRUE_GREEN) == '#00FF00'
    assert str(Color.TRUE_BLUE) == '#0000FF'
    assert str(Color.TRUE_BLACK) == '#000000'


def test_repr() -> None:
    assert repr(Color.TRUE_RED) == 'Color(0xFF0000)'
    assert repr(Color.TRUE_GREEN) == 'Color(0x00FF00)'
    assert repr(Color.TRUE_BLUE) == 'Color(0x0000FF)'
    assert repr(Color.TRUE_BLACK) == 'Color(0x000000)'
