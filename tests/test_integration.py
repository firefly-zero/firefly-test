"""The module contains tests for sys.input-test.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator

from firefly_test import CLI, App, Color, Input, Pad
from pytest import fixture


@fixture(scope='module')
def vfs() -> Iterator[Path]:
    with TemporaryDirectory() as tmp_dir:
        vfs_path = Path(tmp_dir) / 'vfs'
        cli = CLI(vfs=vfs_path)
        cli.install('sys.input-test')
        yield vfs_path


@fixture
def app(vfs: Path) -> App:
    app = App('sys.input-test', vfs_path=vfs)
    app.start()
    return app


def test_colors(app: App) -> None:
    app.update()
    allowed_colors = (Color.WHITE, Color.BLACK)
    for color in app.frame:
        assert color in allowed_colors


def test_buttons(app: App) -> None:
    """If a button is pressed, it is shown on the screen.
    """
    app.update()
    assert app.frame.at(0, 0) == Color.WHITE

    assert app.frame.at(185, 100) == Color.WHITE
    app.update(Input(s=True))
    assert app.frame.at(185, 100) == Color.GREEN

    assert app.frame.at(205, 80) == Color.WHITE
    app.update(Input(e=True))
    assert app.frame.at(205, 80) == Color.GREEN

    assert app.frame.at(170, 80) == Color.WHITE
    app.update(Input(w=True))
    assert app.frame.at(170, 80) == Color.GREEN

    assert app.frame.at(185, 60) == Color.WHITE
    app.update(Input(n=True))
    assert app.frame.at(185, 60) == Color.GREEN

    app.update(Input())
    assert app.frame.at(185, 100) == Color.WHITE
    assert app.frame.at(205, 80) == Color.WHITE
    assert app.frame.at(170, 80) == Color.WHITE
    assert app.frame.at(185, 60) == Color.WHITE


def test_button_circle(app: App) -> None:
    """If a button is pressed, it is shown on the screen.
    """
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


def test_snapshots(app: App) -> None:
    """If a button is pressed, it is shown on the screen.
    """
    snapshots = Path(__file__).parent / '.snapshots'

    app.update()
    app.frame.assert_match(snapshots / 'default')

    input = Input(Pad(-300, -400), s=True, e=True, w=True, n=True)
    app.update(input)
    app.frame.assert_match(snapshots / 'all_pressed')
