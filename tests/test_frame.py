from io import BytesIO
import pytest
from firefly_test import Color, Frame


def get_frame() -> Frame:
    buf = [
        0x00, 0x01, 0x02, 0x03,
        0x10, 0x11, 0x12, 0x13,
        0x20, 0x21, 0x22, 0x23,
    ]
    return Frame(buf, width=4)


def test_height() -> None:
    f = get_frame()
    assert f.width == 4
    assert f.height == 3


def test_at() -> None:
    f = get_frame()
    assert f.at(0, 0) == 0x00
    assert f.at(1, 0) == 0x01
    assert f.at(2, 0) == 0x02
    assert f.at(3, 0) == 0x03
    assert f.at(0, 1) == 0x10
    assert f.at(0, 2) == 0x20
    assert f.at(1, 2) == 0x21
    assert f.at(2, 2) == 0x22
    assert f.at(3, 2) == 0x23
    assert f.at(x=3, y=2) == 0x23
    assert f.at(6) == 0x12
    assert type(f.at(6)) is Color


def test_get_sub() -> None:
    f = get_frame()
    s = f.get_sub(x=1, height=2)
    assert s._buf == [
        0x01, 0x02, 0x03,
        0x11, 0x12, 0x13,
    ]


def test_to_dict() -> None:
    f = Frame([91, 92, 93, 92, 94, 91, 92, 95, 95], width=3)
    d = f.to_dict()
    assert d == {
        91: 2,
        92: 3,
        93: 1,
        94: 1,
        95: 2,
    }


def test_to_set() -> None:
    f = Frame([91, 92, 93, 92, 94, 91, 92, 95, 95], width=3)
    s = f.to_set()
    assert s == {91, 92, 93, 94, 95}


def test_read_write_roundtrip() -> None:
    f1 = get_frame()
    buf = BytesIO()
    f1.write(buf)
    buf.seek(0)
    f2 = Frame.read(buf)
    assert f1._buf == f2._buf
    assert f1._width == f2._width
    assert f1 == f2


def test_iter() -> None:
    buf = [91, 92, 93, 94]
    f = Frame(buf, width=2)
    assert list(f) == [91, 92, 93, 94]
    for c in f:
        assert type(c) is Color
        assert 91 <= int(c) <= 94


def test_contains() -> None:
    f = get_frame()
    assert 0x01 in f
    assert 0x23 in f
    assert 0x24 not in f
    assert 0x30 not in f

    assert Color(0x22) in f
    assert Color(0x32) not in f
    with pytest.raises(TypeError):
        assert '' in f


def test_getitem() -> None:
    f = get_frame()
    assert f[0, 0] == 0x00
    assert f[1, 0] == 0x01
    assert f[2, 0] == 0x02
    assert f[3, 0] == 0x03
    assert f[0, 1] == 0x10
    assert f[0, 2] == 0x20
    assert f[1, 2] == 0x21
    assert f[2, 2] == 0x22
    assert f[3, 2] == 0x23
    with pytest.raises(IndexError):
        f[3, 5]
    with pytest.raises(IndexError):
        f[4, 0]
    with pytest.raises(IndexError):
        f[20]
    assert f[6] == 0x12
    assert type(f[6]) is Color


def test_slice() -> None:
    f = get_frame()
    # https://github.com/python/typeshed/issues/8647
    s = f[(1, 0):(4, 2)]  # type: ignore[misc]
    assert s._buf == [
        0x01, 0x02, 0x03,
        0x11, 0x12, 0x13,
    ]


def test_eq() -> None:
    buf = [
        int(Color.BLACK), int(Color.RED), int(Color.GREEN),
        int(Color.BLUE), int(Color.YELLOW), int(Color.WHITE),
    ]
    f = Frame(buf, width=3)
    assert f == f
    assert f == 'K'
    assert f != 'B'
    assert f == 'KR'
    assert f == 'KRG'
    assert f == '  KRG  '
    assert f != 'KRB'
    assert f != 'RG'
    assert f == """
        K
        B
    """
    assert f == """
        KRG
        BYW
    """
    assert f == """
        K R G
        B Y W
    """
    assert f == """
        K.G
        ..W
    """
    assert f == """
        KR
        BY
    """


def test_len() -> None:
    f = get_frame()
    assert len(f) == f.width * f.height
    assert len(f) == 12
