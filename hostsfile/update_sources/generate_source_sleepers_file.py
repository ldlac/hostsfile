import anyio

from hostsfile.update_sources.try_resolve_domain import try_resolve_domain


async def generate_source_sleepers_file(
    sleepers_filepath: anyio.Path, all_domains: list[str]
) -> int:
    async with await sleepers_filepath.open("+w") as sleepers_file:
        await sleepers_file.truncate()

        semaphore = anyio.Semaphore(20)

        async with anyio.create_task_group() as tg:
            for domain in all_domains:
                tg.start_soon(try_resolve_domain, semaphore, sleepers_file, domain)

        await sleepers_file.seek(0)
        return len(await sleepers_file.readlines())
