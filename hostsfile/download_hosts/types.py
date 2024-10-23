from typing import Any, Callable, Coroutine, Tuple, TypedDict


class SourceData(TypedDict):
    name: str
    url: str
    update: bool


DownloadHostsFrom = Callable[..., Coroutine[Any, Any, Tuple[bytes | None, str]]]
