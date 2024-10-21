import anyio

from hostsfile.update_sources.is_domain_valid import is_domain_valid


async def generate_source_domains_file(
    domains_source_file: anyio.Path, source_hosts_content: bytes
) -> list[str]:
    domains: list[str] = []

    async with await domains_source_file.open("+w") as domains_file:
        await domains_file.truncate()

        for line in source_hosts_content.decode().splitlines():
            if not line.startswith("#") and line:
                if "#" in line:
                    new_line = f"{line.split('#')[0]}\n"
                else:
                    new_line = f"{line}\n"

                new_line = new_line.replace("\t", " ")
                domain = new_line.split(" ")[1].rstrip()
                if is_domain_valid(domain):
                    await domains_file.write(f"{domain}\n")
                    domains.append(domain)

    return domains
