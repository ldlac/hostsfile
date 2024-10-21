import anyio
import anyio.to_process
import anyio.to_thread


async def generate_domains_file(all_domains: list[str]):
    out_hosts_filepath = anyio.Path("out/domains")
    async with await out_hosts_filepath.open("+w") as file:
        await file.truncate()
        for domain in all_domains:
            await file.write(f"{domain}\n")
