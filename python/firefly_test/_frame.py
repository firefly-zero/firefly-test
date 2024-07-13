from __future__ import annotations


class Frame:
    __slots__ = ('_buf', )
    _buf: list[int]

    def __init__(self, buf: list[int]) -> None:
        self._buf = buf
