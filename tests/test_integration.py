"""The module contains tests for sys.input-test.
"""
from firefly_test import App, Color, Input


def test_colors() -> None:
    app = App('sys.input-test')
    app.start()
    app.update()
    allowed_colors = (Color.WHITE, Color.LIGHT_GRAY, Color.GRAY)
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
    assert app.frame.at(170, 110) == Color.LIGHT_BLUE

    assert app.frame.at(200, 100) == Color.WHITE
    app.update(Input(b=True))
    assert app.frame.at(200, 100) == Color.LIGHT_BLUE

    assert app.frame.at(170, 80) == Color.WHITE
    app.update(Input(x=True))
    assert app.frame.at(170, 80) == Color.LIGHT_BLUE

    assert app.frame.at(200, 70) == Color.WHITE
    app.update(Input(y=True))
    assert app.frame.at(200, 70) == Color.LIGHT_BLUE

    app.update(Input())
    assert app.frame.at(170, 110) == Color.WHITE
    assert app.frame.at(200, 100) == Color.WHITE
    assert app.frame.at(170, 80) == Color.WHITE
    assert app.frame.at(200, 70) == Color.WHITE
