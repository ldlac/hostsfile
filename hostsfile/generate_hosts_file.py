import time
import anyio
import anyio.to_process
import anyio.to_thread


async def generate_hosts_file(
    out_hosts_filepath: anyio.Path, all_domains: list[str], target_ip: str
):
    async def append_hosts_file_header(file: anyio.AsyncFile[str], domains_count: int):
        await file.write(
            "# Curated domains list provided by ldlac https://github.com/ldlac/hostsfile\n"
        )
        await file.write(
            "# Heavily inspired by StevenBlack https://github.com/StevenBlack/hosts\n"
        )
        await file.write("\n")
        await file.write(
            f"# Date   : {time.strftime('%d %B %Y %H:%M:%S %Z', time.gmtime())}\n"
        )
        await file.write(f"# Domains: {domains_count}\n")
        await file.write("\n")
        await file.write("0.0.0.0 0.0.0.0\n")

    async def append_localhost_file_section(file: anyio.AsyncFile[str]):
        await file.write("127.0.0.1 localhost\n")
        await file.write("::1 localhost\n")
        await file.write("\n")

    # https://superuser.com/questions/932112/is-there-a-maximum-number-of-hostname-aliases-per-line-in-a-windows-hosts-file#answer-932113
    compress = True

    async with await out_hosts_filepath.open("+w") as file:
        await file.truncate()
        await append_hosts_file_header(file, len(all_domains))
        await append_localhost_file_section(file)

        group_count = 9 if compress else 1
        domains = [
            all_domains[i : i + group_count]
            for i in range(0, len(all_domains), group_count)
        ]
        for domain in domains:
            await file.write(f"{target_ip} {' '.join(domain)}\n")
