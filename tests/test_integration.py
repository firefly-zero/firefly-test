"""The module contains tests for sys.input-test.
"""
from pathlib import Path

from firefly_test import App, Color, Input
from firefly_test._input import Pad


def test_colors() -> None:
    app = App('sys.input-test')
    app.start()
    app.update()
    allowed_colors = (Color.WHITE, Color.BLACK)
    for color in app.frame:
        assert color in allowed_colors


def test_buttons() -> None:
    """If a button is pressed, it is shown on the screen.
    """
    app = App('sys.input-test')
    app.start()
    app.update()
    assert app.frame.at(0, 0) == Color.WHITE

    assert app.frame.at(185, 100) == Color.WHITE
    app.update(Input(s=True))
    assert app.frame.at(185, 100) == Color.LIGHT_GREEN

    assert app.frame.at(205, 80) == Color.WHITE
    app.update(Input(e=True))
    assert app.frame.at(205, 80) == Color.LIGHT_GREEN

    assert app.frame.at(170, 80) == Color.WHITE
    app.update(Input(w=True))
    assert app.frame.at(170, 80) == Color.LIGHT_GREEN

    assert app.frame.at(185, 60) == Color.WHITE
    app.update(Input(n=True))
    assert app.frame.at(185, 60) == Color.LIGHT_GREEN

    app.update(Input())
    assert app.frame.at(185, 100) == Color.WHITE
    assert app.frame.at(205, 80) == Color.WHITE
    assert app.frame.at(170, 80) == Color.WHITE
    assert app.frame.at(185, 60) == Color.WHITE


def test_button_circle() -> None:
    """If a button is pressed, it is shown on the screen.
    """
    app = App('sys.input-test')
    app.start()
    app.update()
    circle = app.frame.get_sub(x=177, y=92, width=25, height=25)
    circle.assert_match("""
        KWWWWWWWWWWWWWWWWWWWWWWWW
        WWWWWWWWWKKKKKKWWWWWWWWWW
        WWWWWWKKKKKKKKKKKKWWWWWWW
        WWWWWKKKKWWWWWWKKKKWWWWWW
        WWWWKKKWWWWWWWWWWKKKWWWWW
        WWWKKKWWWWWWWWWWWWKKKWWWW
        WWKKKWWWWWWWWWWWWWWKKKWWW
        WWKKWWWWWWWWWWWWWWWWKKKWW
        WWKKWWWWWWWKKKWWWWWWKKKWW
        WKKWWWWWWWKWWWKWWWWWWKKWW
        WKKWWWWWWWKWWWWWWWWWWKKKW
        WKKWWWWWWWWKKKWWWWWWWKKKW
        WKKWWWWWWWWWWWKWWWWWWKKKW
        WKKWWWWWWWKWWWKWWWWWWKKKW
        WKKWWWWWWWWKKKWWWWWWWKKKW
        WWKKWWWWWWWWWWWWWWWWKKKKW
        WWKKWWWWWWWWWWWWWWWWKKKWW
        WWKKKWWWWWWWWWWWWWWKKKKWW
        WWWKKKWWWWWWWWWWWWKKKKKWW
        WWWWKKKWWWWWWWWWWKKKKKWWW
        WWWWWKKKKWWWWWWKKKKKKWWWW
        WWWWWWKKKKKKKKKKKKKKWWWWW
        WWWWWWWKKKKKKKKKKKKWWWWWW
        WWWWWWWWWWKKKKKKWWWWWWWWW
        WWWWWWWWWWWWWWWWWWWWWWWWW
    """)


def test_snapshots() -> None:
    """If a button is pressed, it is shown on the screen.
    """
    app = App('sys.input-test')
    snapshots = Path(__file__).parent / '.snapshots'
    app.start()

    app.update()
    app.frame.assert_match(snapshots / 'default')

    input = Input(Pad(30, 40), s=True, e=True, w=True, n=True)
    app.update(input)
    app.frame.assert_match(snapshots / 'all_pressed')
