import anyio
import anyio.to_process
import anyio.to_thread

from hostsfile.dns_watcher.windows.build_knowns_domains import (
    build_knowns_domains,
)
from hostsfile.generate_abp_file import generate_abp_file
from hostsfile.generate_diff_file import generate_diff_file
from hostsfile.generate_domains_file import generate_domains_file
from hostsfile.generate_hosts_file import generate_hosts_file
from hostsfile.generate_overlap_file import generate_overlap_file
from hostsfile.types import Command
from hostsfile.update_sources.update_sources import update_sources


async def gather_all_domains(include_sleepers: bool) -> tuple[set[str], int, int]:
    all_domains_count = 0
    sleepers_domains_count = 0
    final_domains: set[str] = set()
    sources_dir = anyio.Path("sources")
    async for dir in sources_dir.iterdir():
        domains_source_file = dir.joinpath("domains")
        if await domains_source_file.exists():
            async with await domains_source_file.open() as file:
                domains = (await file.read()).splitlines()
                all_domains_count += len(domains)
                final_domains.update(domains)

            if not include_sleepers:
                sleepers_source_file = dir.joinpath("sleepers")
                if await sleepers_source_file.exists():
                    async with await sleepers_source_file.open() as sleepers_file:
                        sleepers_domains = [
                            line.split(" ")[0]
                            for line in (await sleepers_file.read()).splitlines()
                        ]
                        sleepers_domains_count += len(sleepers_domains)
                        final_domains.difference_update(sleepers_domains)

    return final_domains, all_domains_count, sleepers_domains_count


async def generate(
    command: Command,
    update: bool,
    update_sleepers: bool,
    force_update_sleepers: bool,
    include_sleepers: bool,
    target_ip: str,
):
    if update:
        await update_sources(update_sleepers, force_update_sleepers)

    final_domains, all_domains_count, sleepers_domains_count = await gather_all_domains(
        include_sleepers
    )

    print(f"Domains found: {all_domains_count}")
    print(f"Sleepers domains found: {sleepers_domains_count}")

    match command:
        case Command.hosts:
            out_hosts_filepath = anyio.Path("out/hosts")
            print(f"Final number of domains: {len(final_domains)}")
            await generate_hosts_file(
                out_hosts_filepath, list(final_domains), target_ip
            )
        case Command.custom_hosts:
            known_domains = await build_knowns_domains(anyio.Path("dns.csv"))
            out_hosts_filepath = anyio.Path("out/custom_hosts")
            print(f"Known domains: {len(known_domains)}")
            final_domains = list(final_domains.intersection(known_domains))
            print(f"Final number of domains: {len(final_domains)}")
            await generate_hosts_file(
                out_hosts_filepath,
                final_domains,
                target_ip,
            )
        case Command.domains:
            await generate_domains_file(list(final_domains))
        case Command.abp:
            await generate_abp_file(list(final_domains))
        case Command.overlap:
            await generate_overlap_file()
        case Command.diff:
            await generate_diff_file()
