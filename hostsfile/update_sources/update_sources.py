import anyio
import anyio.to_process
import anyio.to_thread
from httpx import AsyncClient

from hostsfile.download_hosts.download_hosts import download_hosts
from hostsfile.update_sources.generate_source_domains_file import (
    generate_source_domains_file,
)
from hostsfile.update_sources.generate_source_sleepers_file import (
    generate_source_sleepers_file,
)


async def update_sources(update_sleepers: bool, force_update_sleepers: bool):
    async with AsyncClient() as httpclient:
        sources_dir = anyio.Path("sources")
        async for dir in sources_dir.iterdir():
            download_hosts_from = await download_hosts(dir)
            source_hosts_content, name = await download_hosts_from(httpclient)

            domains_source_file = dir.joinpath("domains")
            domains: list[str] = await generate_source_domains_file(
                domains_source_file, source_hosts_content
            )

            if update_sleepers:
                sleepers_filepath = dir.joinpath("sleepers")
                if await sleepers_filepath.exists() and not force_update_sleepers:
                    print("Sleepers not updated")
                else:
                    print(f"Updating {name} sleepers domains")
                    sleepers_count = await generate_source_sleepers_file(
                        sleepers_filepath, domains
                    )

                    print(f"Found {sleepers_count} sleepers ")
