import json
from anyio import Path
from httpx import AsyncClient

from hostsfile.download_hosts.types import SourceData, DownloadHostsFrom


BASE_URL = "https://raw.githubusercontent.com"


def download_hosts_from_github(
    source_file: Path,
) -> DownloadHostsFrom:
    async def _download_hosts_from_github(httpclient: AsyncClient):
        async with await source_file.open() as file:
            source = await file.read()
            data: SourceData = json.loads(source)
            url = f"{BASE_URL}/{data['url']}"

            print(f"Updating {data['name']} from {url}")
            content = await httpclient.get(url)

            content.raise_for_status()
            return content.content, data["name"]

    return _download_hosts_from_github
