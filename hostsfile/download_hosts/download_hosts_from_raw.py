import json
from anyio import Path
from httpx import AsyncClient

from hostsfile.download_hosts.types import SourceData, DownloadHostsFrom

EXPECTED_STATUS_CODES = {"https://someonewhocares.org/hosts/zero/hosts/": 404}


def download_hosts_from_raw(
    source_file: Path,
) -> DownloadHostsFrom:
    async def _download_hosts_from_raw(httpclient: AsyncClient):
        async with await source_file.open() as file:
            source = await file.read()
            data: SourceData = json.loads(source)
            url = data["url"]

            print(f"Updating {data['name']} from {url}")
            response = await httpclient.get(url)

            if status_code := EXPECTED_STATUS_CODES.get(url, None):
                assert response.status_code == status_code
            else:
                response.raise_for_status()
            return response.content, data["name"]

    return _download_hosts_from_raw
