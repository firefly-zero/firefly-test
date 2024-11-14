"""The module contains tests for sys.input-test.
"""
from pathlib import Path

from firefly_test import App, Color, Input
from firefly_test._input import Pad


def test_colors() -> None:
    app = App('sys.input-test')
    app.start()
    app.update()
    allowed_colors = (Color.WHITE, Color.DARK_BLUE, Color.GRAY)
    for color in app.frame:
        assert color in allowed_colors


def test_buttons() -> None:
    """If a button is pressed, it is shown on the screen.
    """
    app = App('sys.input-test')
    app.start()
    app.update()
    assert app.frame.at(0, 0) == Color.WHITE

    assert app.frame.at(170, 110) == Color.WHITE
    app.update(Input(a=True))
    assert app.frame.at(170, 110) == Color.DARK_BLUE

    assert app.frame.at(200, 100) == Color.WHITE
    app.update(Input(b=True))
    assert app.frame.at(200, 100) == Color.DARK_BLUE

    assert app.frame.at(170, 80) == Color.WHITE
    app.update(Input(x=True))
    assert app.frame.at(170, 80) == Color.DARK_BLUE

    assert app.frame.at(200, 70) == Color.WHITE
    app.update(Input(y=True))
    assert app.frame.at(200, 70) == Color.DARK_BLUE

    app.update(Input())
    assert app.frame.at(170, 110) == Color.WHITE
    assert app.frame.at(200, 100) == Color.WHITE
    assert app.frame.at(170, 80) == Color.WHITE
    assert app.frame.at(200, 70) == Color.WHITE


def test_button_circle() -> None:
    """If a button is pressed, it is shown on the screen.
    """
    app = App('sys.input-test')
    app.start()
    app.update()
    circle = app.frame.get_sub(x=160, y=100, width=20, height=20)
    circle.assert_match("""
        WWWWddddddddddddWWWW
        WWWddddWWWWWWddddWWW
        WWdddWWWWWWWWWWdddWW
        WdddWWWWWWWWWWWWdddW
        dddWWWWWWWWWWWWWWddd
        ddWWWWWWWWWWWWWWWWdd
        ddWWWWWWWWWWWWWWWWdd
        dWWWWWWWWWWWWWWWWWWd
        dWWWWWWWWWWWWWWWWWWd
        dWWWWWWWWWWWWWWWWWWd
        dWWWWWWWWWWWWWWWWWWd
        dWWWWWWWWWWWWWWWWWWd
        dWWWWWWWWWWWWWWWWWWd
        ddWWWWWWWWWWWWWWWWdd
        ddWWWWWWWWWWWWWWWWdd
        dddWWWWWWWWWWWWWWddd
        WdddWWWWWWWWWWWWdddW
        WWdddWWWWWWWWWWdddWW
        WWWddddWWWWWWddddWWW
        WWWWddddddddddddWWWW
    """)


def test_snapshots() -> None:
    """If a button is pressed, it is shown on the screen.
    """
    app = App('sys.input-test')
    snapshots = Path(__file__).parent / '.snapshots'
    app.start()

    app.update()
    app.frame.assert_match(snapshots / 'default')

    app.update(Input(Pad(30, 40), a=True, b=True, x=True, y=True))
    app.frame.assert_match(snapshots / 'all_pressed')
