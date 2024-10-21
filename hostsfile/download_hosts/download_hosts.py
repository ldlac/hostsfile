from anyio import Path

from hostsfile.download_hosts.download_hosts_from_raw import download_hosts_from_raw
from hostsfile.download_hosts.download_hosts_from_github import (
    download_hosts_from_github,
)
from hostsfile.download_hosts.types import DownloadHostsFrom


async def download_hosts(dir: Path) -> DownloadHostsFrom:
    if (
        github_source_file := dir.joinpath("github.json")
    ) and await github_source_file.exists():
        return download_hosts_from_github(github_source_file)
    elif (
        raw_source_file := dir.joinpath("raw.json")
    ) and await raw_source_file.exists():
        return download_hosts_from_raw(raw_source_file)
    else:
        raise NotImplementedError()
