from typing import Any, Callable, Coroutine, Tuple, TypedDict


class SourceData(TypedDict):
    name: str
    url: str


DownloadHostsFrom = Callable[..., Coroutine[Any, Any, Tuple[bytes, str]]]
