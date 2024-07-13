from __future__ import annotations

from pathlib import Path
import firefly_test._rust as rust


class Frame:
    __slots__ = ('_frame', )


class Runner:
    __slots__ = ('_runner', '_author_id', '_app_id', '_vfs_path')
    _runner: rust.Runner
    _author_id: str
    _app_id: str
    _vfs_path: Path

    def __init__(
        self,
        id: str | tuple[str, str],
        vfs_path: Path,
    ) -> None:
        if isinstance(id, str):
            left, right = id.split('.', maxsplit=1)
            id = (left, right)
        self._author_id, self._app_id = id
        self._vfs_path = vfs_path
        self._runner = rust.Runner(
            author_id=self._author_id,
            app_id=self._app_id,
            vfs_path=str(vfs_path.resolve()),
        )

    @property
    def frame(self) -> Frame:
        raise NotImplementedError
