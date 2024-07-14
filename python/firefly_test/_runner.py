from __future__ import annotations

from pathlib import Path

import firefly_test._rust as rust
from firefly_test._frame import Frame


class ExitedError(Exception):
    """Raised from Firefly.update if the app exits.
    """
    pass


class Firefly:
    __slots__ = (
        '_runner',
        '_author_id',
        '_app_id',
        '_vfs_path',
        '_started',
        '_exited',
    )
    _runner: rust.Runner
    _author_id: str
    _app_id: str
    _vfs_path: Path
    _started: bool
    _exited: bool

    def __init__(
        self,
        id: str | tuple[str, str],
        vfs_path: Path,
    ) -> None:
        if isinstance(id, str):
            left, sep, right = id.partition('.')
            assert sep == '.'
            id = (left, right)
        self._author_id, self._app_id = id
        assert 0 < len(self._author_id) <= 16
        assert 0 < len(self._app_id) <= 16
        self._vfs_path = vfs_path
        self._started = False
        self._exited = False
        self._runner = rust.Runner(
            author_id=self._author_id,
            app_id=self._app_id,
            vfs_path=str(vfs_path.resolve()),
        )

    def start(self) -> None:
        if self._exited:
            raise RuntimeError('trying to start exited app')
        if self._started:
            raise RuntimeError('trying to start already started app')
        self._started = True
        self._runner.start()

    def update(self) -> None:
        if self._exited:
            raise RuntimeError('trying to update exited app')
        exit = self._runner.update()
        if exit:
            self._exited = True
            raise ExitedError

    def get_frame(self) -> Frame:
        buf = self._runner.get_frame()
        return Frame(buf, width=240)
