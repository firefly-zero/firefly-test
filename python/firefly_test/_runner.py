import firefly_test._rust as rust


class Frame:
    __slots__ = ('_frame', )


class Runner:
    __slots__ = ('_runner', '_id')
    _runner: rust.Runner
    _id: str

    def __init__(self, id: str) -> None:
        self._id = id
        self._runner = rust.Runner(id=id)

    @property
    def frame(self) -> Frame:
        raise NotImplementedError
