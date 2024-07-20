# firefly-test

Framework for writing tests for Firefly Zero apps. This is a Python library, so the tests using it are writtten in Pytohn as well. However, you can test a Firefly Zero app or game written in any language, not just Python.

If you don't know Python, don't panic: it's a simple language for simple tasks, and you can learn it good enoug to write your first tests in a matter of minutes. And this documentation will help you.

## Installation

```bash
python3 -m pip install firefly-test
```

Installation from the source is currently not possible: the project depends on `firefly-runtime` which is not open-sourced yet (but will be soon). The wheel distributions on PyPI contain the compiled binaries for the runtime.

## Writing tests in Python

The most popular and simple tool for running Python tests is [pytest](https://docs.pytest.org/en/). Make sure you have it installed:

```bash
python3 -m pip install pytest
```

Tests should be placed in the `tests` directory in the root of the project. Each file with tests should start with `test_`. And each test function also should start with `test_`. For example, create `tests/test_math.py`:

```python
import math

def test_cos():
    assert math.cos(0.0) == 1.0
```

Now, run the tests:

```bash
pytest
```

You can read more in the pytest documentation: [docs.pytest.org](https://docs.pytest.org/en/).

## Installing your app

The framework tests not your source code but a compiled and installed app. So, first, make sure to build and install your project:

```bash
firefly_cli build
```

In the examples below, we'll be using [sys.input-test](https://catalog.fireflyzero.com/sys.input-test) as our test target. If you want to follow along, make sure you have it installed:

```bash
firefly_cli import sys.input-test
```

## Using firefly-test

The `App` class accepts the ID of the app you want to test and provides methods and attributes for interacting with the app:

```python
from firefly_test import App
app = App('sys.input-test')
```

The first thing you should do is `start` your app. It will initialize the app memory, call the `boot` callback, etc.

```python
app.start()
```

Now each time you call `update`, it will run one update cycle: call the `update` and `render` app callbacks, read inputs, flash the image from the frame buffer on the fake screen, etc.

```python
app.update()
```

After the update, you can access the frame buffer using the `frame` attribute. The frame has a lot of helpful methods for checking the image it contains. For example, you can use the `at` method to get the color value of the pixel at the given coordinates:

```python
from firefly_test import Color
assert app.frame.at(x=0, y=0) == Color.WHITE
```

we can iterate over all pixels and, for example, check that every pixel is one of the 3 expected colors:

```python
allowed_colors = (Color.WHITE, Color.LIGHT_GRAY, Color.GRAY)
for color in app.frame:
    assert color in allowed_colors
```

The `update` method may also accept `Input`. This is the input value that this and all subsequent colors will receive (until overwritten). For example, check that pressing the `A` button changes the color fo the pixel (x=170, y=110) from white to light blue:

```python
assert app.frame.at(170, 110) == Color.WHITE
app.update(Input(a=True))
assert app.frame.at(170, 110) == Color.LIGHT_BLUE
```

You can find this test (and the others covered below) in the [tests/test_integration.py](./tests/test_integration.py) file.

## Pattern testing

You can assert that a subregion of a frame matches a pattern. A pattern is an ASCII where each symbols represent an expected color:

* `.`: any color.
* `K`: black.
* `P`: purple.
* `R`: red.
* `O`: orange.
* `Y`: yellow.
* `G`: green.
* `g`: light green.
* `D`: dark green.
* `B`: blue.
* `d`: dark blue.
* `b`: light blue.
* `C`: cyan.
* `W`: white.
* `◔`: light gray.
* `◑`: gray.
* `◕`: dark gray.

Take a frame subregion:

```python
circle = app.frame.get_sub(x=160, y=100, width=20, height=20)
```

Assert that it matches a pattern:

```python
circle.assert_match("""
    WWWW◑◑◑◑◑◑◑◑◑◑◑◑WWWW
    WWW◑◑◑◑WWWWWW◑◑◑◑WWW
    WW◑◑◑WWWWWWWWWW◑◑◑WW
    W◑◑◑WWWWWWWWWWWW◑◑◑W
    ◑◑◑WWWWWWWWWWWWWW◑◑◑
    ◑◑WWWWWWWWWWWWWWWW◑◑
    ◑◑WWWWWWWWWWWWWWWW◑◑
    ◑WWWWWWWWWWWWWWWWWW◑
    ◑WWWWWWWWWWWWWWWWWW◑
    ◑WWWWWWWWWWWWWWWWWW◑
    ◑WWWWWWWWWWWWWWWWWW◑
    ◑WWWWWWWWWWWWWWWWWW◑
    ◑WWWWWWWWWWWWWWWWWW◑
    ◑◑WWWWWWWWWWWWWWWW◑◑
    ◑◑WWWWWWWWWWWWWWWW◑◑
    ◑◑◑WWWWWWWWWWWWWW◑◑◑
    W◑◑◑WWWWWWWWWWWW◑◑◑W
    WW◑◑◑WWWWWWWWWW◑◑◑WW
    WWW◑◑◑◑WWWWWW◑◑◑◑WWW
    WWWW◑◑◑◑◑◑◑◑◑◑◑◑WWWW
""")
```

In this example, we checked that the selected region is a gray circle on a white background.

## Snapshot testing

...

## License

[MIT License](./LICENSE). You can freely use it for testing any apps and games, free or commercial, open-source or proprietary. Happy hacking!
